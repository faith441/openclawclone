# Email Marketing Automation

Automated email marketing sequences with lead management and personalized outreach.

## Features

- Import leads from CSV or Google Sheets
- Template-based personalized emails (Jinja2 support)
- Multi-step drip campaigns with delays
- Rate limiting to avoid spam flags
- Engagement tracking (sent, opened, clicked, replied)
- Gmail API or SMTP support

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up Google Cloud credentials
# 1. Go to https://console.cloud.google.com
# 2. Create a project
# 3. Enable Gmail API and Google Sheets API
# 4. Create OAuth 2.0 credentials
# 5. Download credentials.json
# 6. Place at ~/.config/email-marketing/credentials.json
```

## Quick Start

```bash
# Set environment variables
export EMAIL_SENDER="your@email.com"
export GOOGLE_CREDENTIALS_PATH="~/.config/email-marketing/credentials.json"

# Import leads
python scripts/campaign.py import-leads contacts.csv

# Create campaign
python scripts/campaign.py create "Welcome Series" --template welcome.html

# Run campaign (dry-run first)
python scripts/campaign.py run "Welcome Series" --dry-run
python scripts/campaign.py run "Welcome Series"

# View stats
python scripts/campaign.py stats "Welcome Series"
```

## Documentation

See [SKILL.md](SKILL.md) for full documentation.
