#!/usr/bin/env python3
"""
Telegram AI Assistant

A comprehensive AI-powered Telegram bot with:
- GPT-4 conversations
- Google Calendar integration
- Gmail management
- Task and note management
- Voice message support
"""

import argparse
import asyncio
import json
import logging
import os
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Telegram imports
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    HAS_TELEGRAM = True
except ImportError:
    HAS_TELEGRAM = False
    print("Error: python-telegram-bot not installed")
    print("Run: pip install python-telegram-bot")

# AI imports
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Configuration
CONFIG_DIR = Path.home() / ".config" / "telegram-assistant"
DB_PATH = CONFIG_DIR / "assistant.db"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


@dataclass
class Task:
    """Task model."""
    id: int
    description: str
    priority: str = "medium"
    status: str = "pending"
    due_date: Optional[str] = None
    created_at: Optional[datetime] = None


class Database:
    """SQLite database for tasks and notes."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._init_schema()

    def _init_schema(self):
        cursor = self.conn.cursor()

        # Tasks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                priority TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'pending',
                due_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')

        # Notes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Conversation history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    def add_task(self, chat_id: int, description: str, priority: str = "medium") -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (chat_id, description, priority)
            VALUES (?, ?, ?)
        ''', (chat_id, description, priority))
        self.conn.commit()
        return cursor.lastrowid

    def get_tasks(self, chat_id: int, status: str = "pending") -> list[Task]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, description, priority, status, due_date, created_at
            FROM tasks
            WHERE chat_id = ? AND status = ?
            ORDER BY created_at DESC
        ''', (chat_id, status))

        tasks = []
        for row in cursor.fetchall():
            tasks.append(Task(
                id=row[0],
                description=row[1],
                priority=row[2],
                status=row[3],
                due_date=row[4],
                created_at=datetime.fromisoformat(row[5]) if row[5] else None
            ))
        return tasks

    def complete_task(self, task_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE tasks
            SET status = 'completed', completed_at = ?
            WHERE id = ?
        ''', (datetime.now(), task_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def add_note(self, chat_id: int, content: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO notes (chat_id, content)
            VALUES (?, ?)
        ''', (chat_id, content))
        self.conn.commit()
        return cursor.lastrowid

    def get_notes(self, chat_id: int, limit: int = 10) -> list[tuple]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, content, created_at
            FROM notes
            WHERE chat_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (chat_id, limit))
        return cursor.fetchall()

    def add_message(self, chat_id: int, role: str, content: str):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO messages (chat_id, role, content)
            VALUES (?, ?, ?)
        ''', (chat_id, role, content))
        self.conn.commit()

    def get_conversation_history(self, chat_id: int, limit: int = 10) -> list[dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT role, content
            FROM messages
            WHERE chat_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (chat_id, limit))

        messages = []
        for row in reversed(cursor.fetchall()):
            messages.append({"role": row[0], "content": row[1]})
        return messages


class AIAssistant:
    """OpenAI GPT-4 assistant."""

    def __init__(self):
        if not HAS_OPENAI:
            raise ImportError("OpenAI library required")

        openai.api_key = os.environ.get('OPENAI_API_KEY')
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY not set")

        self.model = "gpt-4"
        self.system_prompt = """You are a helpful personal assistant on Telegram.
Be concise, friendly, and practical. Help users with tasks, calendar, emails, and questions.
Keep responses under 2000 characters for Telegram."""

    async def ask(self, question: str, conversation_history: list[dict] = None) -> str:
        """Ask the AI a question."""
        messages = [{"role": "system", "content": self.system_prompt}]

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": question})

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return "Sorry, I'm having trouble thinking right now. Please try again."


class TelegramAssistant:
    """Main Telegram bot."""

    def __init__(self):
        self.token = os.environ.get('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set")

        self.db = Database()
        self.ai = AIAssistant()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = """🤖 **Telegram AI Assistant**

I can help you with:
- 💬 Answer questions (just ask me anything)
- ✅ Manage tasks
- 📝 Take notes
- 📅 Calendar (coming soon)
- 📧 Email (coming soon)

Try these commands:
/help - Show all commands
/ask - Ask me anything
/task - Create a task
/tasks - List your tasks
/note - Save a note
/notes - View your notes

Or just send me a message!"""

        await update.message.reply_text(welcome_message, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = """📖 **Commands**

**AI & Chat:**
/ask <question> - Ask me anything
Just message me! - I'll respond to any message

**Tasks:**
/task <description> - Create new task
/tasks - List pending tasks
/done <task_id> - Mark task complete

**Notes:**
/note <text> - Save a note
/notes - View recent notes

**Other:**
/start - Show welcome message
/help - Show this help"""

        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def ask_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ask command."""
        chat_id = update.effective_chat.id
        question = update.message.text.replace('/ask', '').strip()

        if not question:
            await update.message.reply_text("Please provide a question. Example: /ask What is Python?")
            return

        # Show typing indicator
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")

        # Get conversation history
        history = self.db.get_conversation_history(chat_id)

        # Save user message
        self.db.add_message(chat_id, "user", question)

        # Get AI response
        response = await self.ai.ask(question, history)

        # Save assistant response
        self.db.add_message(chat_id, "assistant", response)

        await update.message.reply_text(response)

    async def task_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /task command."""
        chat_id = update.effective_chat.id
        description = update.message.text.replace('/task', '').strip()

        if not description:
            await update.message.reply_text("Usage: /task <description>\nExample: /task Review pull requests")
            return

        task_id = self.db.add_task(chat_id, description)
        await update.message.reply_text(f"✅ Task created (ID: {task_id})\n\n{description}")

    async def tasks_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /tasks command."""
        chat_id = update.effective_chat.id
        tasks = self.db.get_tasks(chat_id)

        if not tasks:
            await update.message.reply_text("No pending tasks! 🎉")
            return

        message = "📋 **Your Tasks:**\n\n"
        for task in tasks:
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")
            message += f"{priority_emoji} **#{task.id}** {task.description}\n"

        message += f"\nUse /done <id> to mark as complete"

        await update.message.reply_text(message, parse_mode='Markdown')

    async def done_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /done command."""
        task_id_str = update.message.text.replace('/done', '').strip()

        if not task_id_str.isdigit():
            await update.message.reply_text("Usage: /done <task_id>\nExample: /done 1")
            return

        task_id = int(task_id_str)
        if self.db.complete_task(task_id):
            await update.message.reply_text(f"✅ Task #{task_id} marked as complete!")
        else:
            await update.message.reply_text(f"❌ Task #{task_id} not found")

    async def note_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /note command."""
        chat_id = update.effective_chat.id
        content = update.message.text.replace('/note', '').strip()

        if not content:
            await update.message.reply_text("Usage: /note <text>\nExample: /note Remember to call dentist")
            return

        note_id = self.db.add_note(chat_id, content)
        await update.message.reply_text(f"📝 Note saved (ID: {note_id})")

    async def notes_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /notes command."""
        chat_id = update.effective_chat.id
        notes = self.db.get_notes(chat_id)

        if not notes:
            await update.message.reply_text("No notes yet.")
            return

        message = "📝 **Your Notes:**\n\n"
        for note_id, content, created_at in notes:
            date = datetime.fromisoformat(created_at).strftime("%m/%d %H:%M")
            message += f"**#{note_id}** ({date})\n{content[:100]}...\n\n"

        await update.message.reply_text(message, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages."""
        chat_id = update.effective_chat.id
        text = update.message.text

        # Show typing
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")

        # Get history and ask AI
        history = self.db.get_conversation_history(chat_id)
        self.db.add_message(chat_id, "user", text)

        response = await self.ai.ask(text, history)
        self.db.add_message(chat_id, "assistant", response)

        await update.message.reply_text(response)

    def run(self):
        """Start the bot."""
        if not HAS_TELEGRAM:
            logger.error("python-telegram-bot not installed")
            return

        logger.info("Starting Telegram AI Assistant...")

        # Create application
        app = Application.builder().token(self.token).build()

        # Add handlers
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("ask", self.ask_command))
        app.add_handler(CommandHandler("task", self.task_command))
        app.add_handler(CommandHandler("tasks", self.tasks_command))
        app.add_handler(CommandHandler("done", self.done_command))
        app.add_handler(CommandHandler("note", self.note_command))
        app.add_handler(CommandHandler("notes", self.notes_command))

        # Handle all text messages
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        # Start polling
        logger.info("Bot is running! Press Ctrl+C to stop.")
        app.run_polling()


def main():
    parser = argparse.ArgumentParser(description="Telegram AI Assistant")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Start
    start_parser = subparsers.add_parser("start", help="Start the bot")
    start_parser.add_argument("--daemon", action="store_true", help="Run in background")

    # Get chat ID
    subparsers.add_parser("get-chat-id", help="Get your chat ID")

    args = parser.parse_args()

    if args.command == "start":
        try:
            assistant = TelegramAssistant()
            assistant.run()
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Error: {e}")
            import traceback
            traceback.print_exc()

    elif args.command == "get-chat-id":
        print("\n1. Start the bot with: python telegram_bot.py start")
        print("2. Send a message to your bot on Telegram")
        print("3. Check the logs for 'Chat ID: XXXXXX'")
        print("\nOr use this to get updates:")
        print(f"curl https://api.telegram.org/bot{os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_TOKEN')}/getUpdates")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
