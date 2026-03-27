---
name: telegram-ai-assistant
description: Complete AI assistant on Telegram integrating GPT-4, Google Calendar, Gmail, and task management. Handles voice/text inputs, email summaries, calendar events, and tasks.
---

# Telegram AI Assistant

## Overview

A comprehensive AI-powered Telegram bot that serves as your personal assistant. Integrates GPT-4 for natural conversations, Google Calendar for scheduling, Gmail for email management, and database storage for tasks and notes. Supports both text and voice messages.

## When to Use

- User wants an AI assistant accessible via Telegram
- User needs calendar management through chat
- User wants email summaries and quick replies
- User needs voice-to-text note taking
- User wants task management via chat commands
- User needs a unified interface for multiple services

## Features

- **AI Conversations**: GPT-4 powered natural language understanding
- **Voice Support**: Process voice messages with speech-to-text
- **Calendar Integration**: Schedule, view, and manage calendar events
- **Email Management**: Read summaries, send emails, search inbox
- **Task Management**: Create, list, and complete tasks
- **Notes**: Quick note taking with search
- **Reminders**: Set reminders for specific times
- **Multi-modal**: Handle text, voice, images, and documents

## Quick Start

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN="your-bot-token"
export OPENAI_API_KEY="sk-..."
export GOOGLE_CREDENTIALS_PATH="~/.config/telegram-assistant/credentials.json"
```

### Get Telegram Bot Token

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot`
3. Follow instructions to create your bot
4. Copy the bot token

### Get Your Chat ID

```bash
# Start the bot first, then send it a message
# Run this to see your chat ID:
python scripts/telegram_bot.py get-chat-id
```

## Usage

### Start the Bot

```bash
# Interactive mode
python scripts/telegram_bot.py start

# Daemon mode (background)
python scripts/telegram_bot.py start --daemon

# With specific chat ID
python scripts/telegram_bot.py start --chat-id YOUR_CHAT_ID
```

### Telegram Commands

```
/start - Start the assistant
/help - Show all commands
/ask <question> - Ask the AI anything
/calendar - View today's calendar
/event <title> <time> - Create calendar event
/email - Get email summary
/send <to> <message> - Send email
/task <description> - Create task
/tasks - List all tasks
/done <task_id> - Mark task as complete
/note <text> - Save a note
/notes - View all notes
/remind <time> <message> - Set reminder
/search <query> - Search notes and tasks
```

### Natural Language Examples

```
User: Schedule a meeting with John tomorrow at 2pm
Bot: ✅ Created event "Meeting with John" for tomorrow at 2:00 PM

User: What's on my calendar today?
Bot: 📅 Today's Schedule:
     9:00 AM - Team Standup
     2:00 PM - Client Call
     4:30 PM - Code Review

User: Summarize my emails from today
Bot: 📧 Email Summary (5 new):
     - Invoice from Acme Corp
     - Meeting notes from Sarah
     - ...

User: Send an email to john@example.com saying the report is ready
Bot: ✉️ Email sent to john@example.com

User: [Voice message: "Remind me to call the dentist tomorrow"]
Bot: 🔔 Reminder set: "Call the dentist" for tomorrow at 9:00 AM
```

## Bot Commands

### AI Conversation

```python
# Natural conversation
User: What's the weather like in San Francisco?
Bot: [AI generates response using GPT-4]

# Context-aware
User: Tell me about quantum computing
Bot: [Detailed explanation]
User: What are some applications?
Bot: [Follows up on previous context]
```

### Calendar Management

```
# View calendar
/calendar                    # Today
/calendar tomorrow           # Tomorrow
/calendar week               # This week
/calendar 2024-03-28         # Specific date

# Create events
/event Team meeting tomorrow 2pm
/event "Lunch with Sarah" 2024-03-28 12:30
/event Conference call 15:00 duration:1h

# Update events
/cancel next meeting
/reschedule morning meeting to 3pm
```

### Email Operations

```
# Get summaries
/email                       # Today's emails
/email unread                # Unread only
/email from:john@example.com # Specific sender
/email subject:invoice       # Search subject

# Send emails
/send john@example.com Check out this report
/send to:team@company.com subject:"Weekly Update" Body text here

# Quick replies
/reply latest Thanks for the update
```

### Task Management

```
# Create tasks
/task Review pull requests
/task "Prepare Q1 report" priority:high due:friday
/task Call dentist +health +urgent

# List tasks
/tasks                       # All tasks
/tasks today                 # Due today
/tasks priority:high         # By priority
/tasks tag:work              # By tag

# Complete tasks
/done 1                      # Mark task #1 done
/done review pull requests   # By description
```

### Notes & Search

```
# Save notes
/note Meeting notes: discussed Q1 targets
/note [Send with file attachment]

# View notes
/notes                       # All notes
/notes recent                # Recent 10
/notes today                 # Today's notes

# Search everything
/search quantum              # Search notes and tasks
/search tag:work             # By tag
```

## Configuration

Create `~/.config/telegram-assistant/config.yaml`:

```yaml
# Telegram settings
telegram:
  bot_token: "${TELEGRAM_BOT_TOKEN}"
  allowed_chat_ids:           # Optional: restrict to specific users
    - 123456789
    - 987654321

# AI settings
ai:
  provider: openai
  model: gpt-4
  temperature: 0.7
  max_tokens: 1000
  system_prompt: |
    You are a helpful personal assistant. Be concise, friendly, and proactive.
    You can help with calendars, emails, tasks, and general questions.

# Google integration
google:
  credentials_path: "~/.config/telegram-assistant/credentials.json"
  calendar:
    enabled: true
    default_duration: 30  # minutes
    timezone: "America/New_York"
  gmail:
    enabled: true
    max_summary: 10       # Max emails in summary

# Task management
tasks:
  database: "~/.config/telegram-assistant/tasks.db"
  default_priority: medium
  tags_enabled: true

# Voice settings
voice:
  enabled: true
  language: "en-US"
  transcription: openai-whisper  # or google-speech

# Reminders
reminders:
  enabled: true
  check_interval: 60     # seconds
  default_time: "09:00"  # If no time specified

# Advanced
logging:
  level: INFO
  file: "~/.config/telegram-assistant/bot.log"

features:
  conversation_history: true
  max_history: 20
  summarize_long_responses: true
```

## Code Examples

### Python - Basic Bot

```python
from telegram_assistant import TelegramAssistant

# Initialize
assistant = TelegramAssistant(
    telegram_token="YOUR_BOT_TOKEN",
    openai_key="YOUR_OPENAI_KEY"
)

# Start bot
assistant.start()
```

### Python - Custom Handlers

```python
from telegram_assistant import TelegramAssistant, CommandHandler

assistant = TelegramAssistant()

# Custom command
@assistant.command("weather")
def handle_weather(message):
    """Get weather information."""
    location = message.text.replace("/weather", "").strip()
    weather_info = get_weather(location)
    return f"Weather in {location}: {weather_info}"

# Custom text handler
@assistant.on_text(r"what.*time")
def handle_time_question(message):
    """Respond to time questions."""
    return f"Current time: {datetime.now().strftime('%I:%M %p')}"

assistant.start()
```

### Python - Integration Example

```python
from telegram_assistant import TelegramAssistant
from telegram_assistant.integrations import GoogleCalendar, Gmail, TaskManager

assistant = TelegramAssistant()

# Add integrations
assistant.add_integration(GoogleCalendar())
assistant.add_integration(Gmail())
assistant.add_integration(TaskManager())

# Handle calendar queries
@assistant.command("schedule")
async def schedule_meeting(message, calendar):
    """Schedule a meeting using AI to parse the request."""
    ai_response = await assistant.ai.parse_event(message.text)

    event = await calendar.create_event(
        title=ai_response.title,
        start=ai_response.start_time,
        duration=ai_response.duration
    )

    return f"✅ Scheduled: {event.title} at {event.start_time}"

assistant.start()
```

### JavaScript/Node.js

```javascript
const { TelegramAssistant } = require('./telegram-assistant');

const assistant = new TelegramAssistant({
  telegramToken: process.env.TELEGRAM_BOT_TOKEN,
  openaiKey: process.env.OPENAI_API_KEY
});

// Handle commands
assistant.command('ask', async (ctx) => {
  const question = ctx.message.text.replace('/ask', '').trim();
  const response = await assistant.ai.ask(question);
  await ctx.reply(response);
});

// Handle voice messages
assistant.on('voice', async (ctx) => {
  const transcript = await assistant.transcribeVoice(ctx.message.voice);
  const response = await assistant.ai.ask(transcript);
  await ctx.reply(`You said: "${transcript}"\n\n${response}`);
});

assistant.start();
```

## Advanced Features

### Voice Message Processing

```python
# Automatic voice transcription
User: [Sends voice message]
Bot: Processing voice message...
Bot: You said: "Schedule a meeting with John tomorrow at 2pm"
Bot: ✅ Created event "Meeting with John" for tomorrow at 2:00 PM
```

### Context-Aware Conversations

```python
# Bot remembers conversation context
User: Tell me about Python
Bot: Python is a high-level programming language...

User: What are some popular frameworks?
Bot: For Python, popular frameworks include Django, Flask, FastAPI...

User: Which one should I use for a REST API?
Bot: For REST APIs, I'd recommend FastAPI because...
```

### Multi-Step Workflows

```python
# Complex task handling
User: Help me plan my day
Bot: Sure! Let me check your calendar...
Bot: You have 3 meetings today. Would you like me to:
     1. Show detailed schedule
     2. Suggest focus time blocks
     3. Check for conflicts
User: 2
Bot: Based on your schedule, here are suggested focus blocks:
     - 10:00-11:30 AM (90 min)
     - 3:00-4:30 PM (90 min)
     Would you like me to block these times?
```

### Email Intelligence

```python
# Smart email categorization
User: /email summary
Bot: 📧 Email Summary (12 new):

     🔴 Urgent (2):
     - Invoice overdue - Acme Corp
     - Production issue - DevOps Team

     🟡 Action Required (3):
     - Meeting confirmation needed - Sarah
     - Document review - Legal Team
     - Expense approval - Finance

     🟢 FYI (7):
     - Newsletter - TechCrunch
     - Team update - Project Manager
     ...
```

## Database Schema

The bot uses SQLite for local storage:

```sql
-- Tasks table
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    chat_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    priority TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'pending',
    due_date TEXT,
    tags TEXT,  -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Notes table
CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    chat_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    tags TEXT,  -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reminders table
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY,
    chat_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    remind_at TIMESTAMP NOT NULL,
    sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversation history
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    chat_id INTEGER NOT NULL,
    role TEXT NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Best Practices

| Practice | Recommendation |
|----------|---------------|
| Security | Use allowed_chat_ids to restrict access |
| API Keys | Store in environment variables, never commit |
| Rate Limits | Implement cooldowns for AI requests |
| Error Handling | Graceful fallbacks for service failures |
| Logging | Log all interactions for debugging |
| Privacy | Inform users about data storage |

## Deployment

### Local Deployment

```bash
# Run in background
nohup python scripts/telegram_bot.py start --daemon &

# Or use systemd service
sudo systemctl start telegram-assistant
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scripts/ ./scripts/
COPY config/ ./config/

CMD ["python", "scripts/telegram_bot.py", "start"]
```

```bash
# Build and run
docker build -t telegram-assistant .
docker run -d \
  -e TELEGRAM_BOT_TOKEN="your-token" \
  -e OPENAI_API_KEY="your-key" \
  -v ./data:/app/data \
  telegram-assistant
```

### Cloud Deployment (Heroku)

```bash
# Procfile
worker: python scripts/telegram_bot.py start

# Deploy
heroku create my-telegram-assistant
heroku config:set TELEGRAM_BOT_TOKEN="your-token"
heroku config:set OPENAI_API_KEY="your-key"
git push heroku main
```

## Webhook vs Polling

### Polling Mode (Default)

```python
# Easier setup, works everywhere
assistant.start(polling=True)
```

### Webhook Mode (Production)

```python
# Better for high-traffic bots
assistant.start(
    webhook=True,
    webhook_url="https://yourdomain.com/webhook",
    port=8443
)
```

## Error Handling

```python
# Graceful error handling
try:
    response = await assistant.ai.ask(question)
except OpenAIError:
    response = "Sorry, I'm having trouble with AI right now. Please try again."
except CalendarError:
    response = "Can't access calendar at the moment. Check back soon."
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    response = "Something went wrong. I've logged the error."
```

## Usage Examples

### Daily Routine Automation

```
# Morning routine
User: /start
Bot: Good morning! Here's your day:

📅 Calendar (3 events)
- 9:00 AM Team Standup
- 2:00 PM Client Call
- 4:00 PM Code Review

📧 Emails (8 new)
- 2 urgent, 3 require action

✅ Tasks (5 pending)
- 2 due today

Would you like details on any of these?
```

### Meeting Preparation

```
User: Prepare me for my 2pm meeting
Bot: 📋 Meeting Prep: "Client Call" at 2:00 PM

📧 Related emails:
- Latest update from client (yesterday)
- Contract discussion (2 days ago)

📝 Previous notes:
- Discussed pricing on March 15
- Follow-up needed on timeline

✅ Action items from last meeting:
- Send proposal (completed ✅)
- Schedule demo (pending)

Anything else you need?
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Bot not responding | Check token, ensure bot is running |
| Calendar errors | Verify Google OAuth credentials |
| Voice not working | Check Whisper API key |
| AI timeouts | Reduce max_tokens or use gpt-3.5-turbo |
| Database errors | Check file permissions on .db file |

## Rate Limits & Costs

- **Telegram Bot API**: Free, unlimited messages
- **OpenAI GPT-4**: ~$0.03 per conversation
- **Google APIs**: Free tier usually sufficient
- **Whisper API**: $0.006 per minute of audio

## Privacy & Security

- All data stored locally in SQLite
- Google credentials use OAuth2
- Restrict bot access using `allowed_chat_ids`
- No data sent to third parties except API calls
- Conversation history can be disabled
