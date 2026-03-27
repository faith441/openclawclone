---
name: email-marketing-automation
description: Automated email marketing sequences with lead management and personalized outreach. Manage campaigns, track engagement, and send templated emails via Gmail API or SMTP.
---

# Email Marketing Automation

## Overview

Automates email marketing workflows including lead management, campaign sequencing, personalized outreach, and engagement tracking. Integrates with Gmail API, SMTP servers, and spreadsheet-based contact lists.

## When to Use

- User wants to send bulk personalized emails
- User needs to manage email sequences/drip campaigns
- User wants to track email campaign performance
- User needs to import/manage leads from spreadsheets
- User wants to schedule automated follow-up emails

## Features

- **Lead Management**: Import contacts from CSV/Google Sheets
- **Template Engine**: Personalized emails with variable substitution
- **Campaign Sequences**: Multi-step drip campaigns with delays
- **Engagement Tracking**: Open rates, click tracking, replies
- **Rate Limiting**: Respects sending limits to avoid spam flags

## Quick Start

### Setup Gmail API

```bash
# Install dependencies
pip install google-auth google-auth-oauthlib google-api-python-client

# Set up OAuth credentials (download from Google Cloud Console)
# Place credentials.json in ~/.config/email-marketing/
```

### Environment Variables

```bash
export EMAIL_SENDER="your@email.com"
export EMAIL_SMTP_HOST="smtp.gmail.com"
export EMAIL_SMTP_PORT="587"
export EMAIL_APP_PASSWORD="your-app-password"  # For SMTP
export GOOGLE_CREDENTIALS_PATH="~/.config/email-marketing/credentials.json"
```

## Usage

### Import Leads

```bash
# From CSV
python scripts/campaign.py import-leads contacts.csv

# From Google Sheets
python scripts/campaign.py import-leads --sheets "Sheet ID" --range "A1:D100"
```

### Create Campaign

```bash
# Create a new campaign
python scripts/campaign.py create "Welcome Series" \
  --template welcome.html \
  --leads leads.csv \
  --delay 2d  # 2 days between emails
```

### Send Emails

```bash
# Send single email
python scripts/campaign.py send --to "user@example.com" --template welcome.html --vars '{"name": "John"}'

# Run campaign
python scripts/campaign.py run "Welcome Series" --dry-run  # Preview first
python scripts/campaign.py run "Welcome Series"            # Actually send
```

### Track Engagement

```bash
# View campaign stats
python scripts/campaign.py stats "Welcome Series"

# Export engagement data
python scripts/campaign.py export-stats "Welcome Series" -o stats.csv
```

## Template Format

Templates support Jinja2-style variable substitution:

```html
<!-- templates/welcome.html -->
Subject: Welcome to {{company_name}}, {{first_name}}!

<html>
<body>
  <h1>Hi {{first_name}},</h1>
  <p>Thanks for signing up for {{company_name}}!</p>
  <p>Here are your next steps:</p>
  <ul>
    <li><a href="{{onboarding_url}}">Complete your profile</a></li>
    <li>Check out our <a href="{{docs_url}}">documentation</a></li>
  </ul>
  <p>Best,<br>{{sender_name}}</p>
</body>
</html>
```

## Lead CSV Format

```csv
email,first_name,last_name,company,tags
john@example.com,John,Doe,Acme Inc,new-signup
jane@example.com,Jane,Smith,Tech Corp,webinar-attendee
```

## Campaign Sequence Example

```yaml
# campaigns/welcome-series.yaml
name: Welcome Series
from: team@company.com
subject_prefix: "[Company]"

sequence:
  - step: 1
    delay: 0  # Immediate
    template: welcome.html
    subject: "Welcome aboard, {{first_name}}!"

  - step: 2
    delay: 2d  # 2 days later
    template: getting-started.html
    subject: "Getting started with {{product_name}}"
    condition: "not opened_step_1"  # Only if didn't open first

  - step: 3
    delay: 5d
    template: check-in.html
    subject: "How's it going, {{first_name}}?"
    condition: "not clicked_any"

settings:
  rate_limit: 50/hour
  skip_weekends: true
  unsubscribe_link: true
```

## Code Examples

### Python - Send Single Email

```python
from email_marketing import EmailClient

client = EmailClient()

# Send personalized email
client.send(
    to="user@example.com",
    template="welcome.html",
    variables={
        "first_name": "John",
        "company_name": "Acme",
        "onboarding_url": "https://example.com/onboard"
    }
)
```

### Python - Run Campaign

```python
from email_marketing import Campaign, LeadManager

# Load leads
leads = LeadManager.from_csv("contacts.csv")

# Create campaign
campaign = Campaign(
    name="Product Launch",
    template="launch.html",
    leads=leads
)

# Preview
for email in campaign.preview(limit=5):
    print(f"To: {email.to}, Subject: {email.subject}")

# Send with rate limiting
campaign.run(rate_limit="30/hour", dry_run=False)
```

### JavaScript/Node.js

```javascript
const { EmailCampaign } = require('./scripts/campaign');

const campaign = new EmailCampaign({
  name: 'Newsletter',
  from: 'newsletter@company.com',
  template: 'newsletter.html'
});

// Add leads
await campaign.importLeads('subscribers.csv');

// Send
await campaign.run({
  rateLimit: 100,
  ratePeriod: 'hour'
});
```

## Best Practices

| Practice | Recommendation |
|----------|---------------|
| Rate Limiting | Max 50-100 emails/hour to avoid spam flags |
| Personalization | Always use recipient's name and relevant context |
| Unsubscribe | Include unsubscribe link in every email |
| Testing | Use `--dry-run` before actual sends |
| Timing | Avoid weekends, send during business hours |
| List Hygiene | Remove bounced emails immediately |

## Output Format

### Campaign Stats

```markdown
## Campaign: Welcome Series

**Status:** Running
**Created:** 2024-03-15
**Total Leads:** 500

### Engagement Metrics

| Metric | Count | Rate |
|--------|-------|------|
| Sent | 450 | 90% |
| Delivered | 445 | 98.9% |
| Opened | 180 | 40.4% |
| Clicked | 45 | 10% |
| Replied | 12 | 2.7% |
| Bounced | 5 | 1.1% |
| Unsubscribed | 3 | 0.7% |

### Sequence Progress

| Step | Template | Sent | Pending |
|------|----------|------|---------|
| 1 | welcome.html | 450 | 50 |
| 2 | getting-started.html | 200 | 250 |
| 3 | check-in.html | 50 | 400 |
```

## Error Handling

- **Rate Limited**: Automatically backs off and retries
- **Bounced**: Marks lead as invalid, skips in future
- **Invalid Email**: Logs error, continues with others
- **Auth Failed**: Prompts for credential refresh
