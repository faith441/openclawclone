# Sales Meeting Follow-Up Automation

Automate sales follow-ups with AI-powered email generation and smart meeting scheduling.

## Features

- Google Calendar integration for meeting tracking
- AI-powered follow-up email generation (GPT-4)
- Smart meeting slot suggestions based on availability
- Human approval workflow for critical actions
- Meeting notes extraction and action items
- Automatic booking with calendar invites

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up credentials
# 1. Google Cloud Console: Enable Calendar API and Gmail API
# 2. Download OAuth credentials.json
# 3. Place at ~/.config/sales-follow-up/credentials.json
```

## Quick Start

```bash
# Set environment variables
export GOOGLE_CREDENTIALS_PATH="~/.config/sales-follow-up/credentials.json"
export OPENAI_API_KEY="sk-..."
export EMAIL_SENDER="you@company.com"
export TIMEZONE="America/New_York"

# Analyze recent meetings
python scripts/follow_up.py analyze --days 7

# Draft follow-up email
python scripts/follow_up.py draft "Meeting with John Doe"

# Suggest meeting slots
python scripts/follow_up.py suggest-slots \
  --attendees "john@example.com" \
  --duration 30 \
  --prefer-morning

# Complete auto workflow (with approval)
python scripts/follow_up.py auto \
  --meeting "Q1 Planning Discussion" \
  --approve-mode interactive
```

## Configuration

Edit `~/.config/sales-follow-up/config.yaml`:

```yaml
email:
  sender: "you@company.com"
  signature: "Best regards,\\nYour Name"

calendar:
  timezone: "America/New_York"
  buffer_minutes: 15
  working_hours:
    start: "09:00"
    end: "17:00"

ai:
  model: "gpt-4"
  temperature: 0.7
```

## Documentation

See [SKILL.md](SKILL.md) for full documentation.
