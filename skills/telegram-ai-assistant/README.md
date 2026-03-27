# Telegram AI Assistant

Complete AI-powered Telegram bot with GPT-4, task management, notes, and future support for calendar and email.

## Features

- AI conversations powered by GPT-4
- Task management (create, list, complete)
- Note taking with timestamps
- Conversation history
- Natural language processing
- Future: Google Calendar, Gmail integration

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Setup

### 1. Create Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy your bot token

### 2. Set Environment Variables

```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export OPENAI_API_KEY="sk-..."
```

### 3. Start the Bot

```bash
python scripts/telegram_bot.py start
```

## Usage

### Commands

```
/start - Welcome message
/help - Show all commands
/ask <question> - Ask AI anything
/task <description> - Create task
/tasks - List pending tasks
/done <task_id> - Complete task
/note <text> - Save note
/notes - View recent notes
```

### Examples

```
# AI conversation
User: What's the capital of France?
Bot: The capital of France is Paris.

# Task management
User: /task Review pull requests
Bot: ✅ Task created (ID: 1)

User: /tasks
Bot: 📋 Your Tasks:
     🟡 #1 Review pull requests

User: /done 1
Bot: ✅ Task #1 marked as complete!

# Notes
User: /note Remember to call dentist tomorrow
Bot: 📝 Note saved (ID: 1)
```

## Documentation

See [SKILL.md](SKILL.md) for full documentation.
