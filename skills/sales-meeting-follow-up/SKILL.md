---
name: sales-meeting-follow-up
description: Automate sales follow-ups using Google Calendar and Gmail. AI suggests meeting slots, sends follow-up emails, and books meetings with human approval workflow.
---

# Sales Meeting Follow-Up Automation

## Overview

Automates sales meeting follow-up workflows including intelligent meeting slot suggestions, automated follow-up emails, calendar integration, and human-in-the-loop approval for critical actions. Uses AI to draft contextual follow-ups based on meeting notes.

## When to Use

- User wants to automate post-meeting follow-ups
- User needs to schedule follow-up meetings automatically
- User wants AI-generated follow-up emails based on meeting context
- User needs to track meeting engagement and responses
- User wants to suggest meeting slots based on calendar availability

## Features

- **Calendar Integration**: Sync with Google Calendar for availability
- **AI Follow-ups**: GPT-powered contextual email generation
- **Smart Scheduling**: Suggest optimal meeting times
- **Human Approval**: Review before booking/sending
- **Meeting Notes**: Extract action items and context
- **CRM Sync**: Track follow-up status (optional)

## Quick Start

### Setup Google Calendar & Gmail API

```bash
# Install dependencies
pip install google-auth google-auth-oauthlib google-api-python-client openai

# Set up OAuth credentials (download from Google Cloud Console)
# Place credentials.json in ~/.config/sales-follow-up/
```

### Environment Variables

```bash
export GOOGLE_CREDENTIALS_PATH="~/.config/sales-follow-up/credentials.json"
export OPENAI_API_KEY="sk-..."
export EMAIL_SENDER="you@company.com"
export TIMEZONE="America/New_York"
```

## Usage

### Analyze Recent Meetings

```bash
# Check meetings from last N days
python scripts/follow_up.py analyze --days 7

# Output: Lists meetings without follow-ups
```

### Generate Follow-up Email

```bash
# AI-generated follow-up based on meeting notes
python scripts/follow_up.py draft "Meeting with John Doe" \
  --notes "Discussed Q1 budget, action items..." \
  --tone professional

# Preview email, approve to send
```

### Suggest Meeting Slots

```bash
# Find available slots for next meeting
python scripts/follow_up.py suggest-slots \
  --attendees "john@example.com,jane@example.com" \
  --duration 30 \
  --days-ahead 14 \
  --prefer-morning

# Outputs: 5 optimal time slots
```

### Book Meeting with Approval

```bash
# Suggest and book follow-up meeting
python scripts/follow_up.py book \
  --attendees "john@example.com" \
  --subject "Q1 Budget Review Follow-up" \
  --duration 30 \
  --auto-suggest

# Shows suggested slots → user approves → books automatically
```

### Auto Follow-up Workflow

```bash
# Run complete follow-up workflow
python scripts/follow_up.py auto \
  --meeting "Meeting with Acme Corp" \
  --suggest-next-meeting \
  --approve-mode interactive

# 1. Drafts follow-up email
# 2. Shows preview → user approves
# 3. Sends email
# 4. Suggests next meeting slots
# 5. Shows slots → user selects
# 6. Books meeting
```

### Batch Process

```bash
# Process all meetings from yesterday
python scripts/follow_up.py batch \
  --date yesterday \
  --require-approval

# Goes through each meeting interactively
```

## AI Follow-up Template

The AI uses meeting context to generate personalized follow-ups:

```
Meeting: Q1 Planning with John Doe, Acme Corp
Duration: 30 min
Notes: Discussed budget allocation, decided to increase marketing spend by 20%.
       John will send proposal by Friday. Need follow-up in 2 weeks.

Generated Email:
---
Subject: Following up on Q1 Planning Discussion

Hi John,

Great connecting yesterday about Q1 planning. I appreciate you taking the time
to discuss the budget allocation strategy.

Key takeaways from our conversation:
• Increasing marketing spend by 20% for Q1
• You'll send the detailed proposal by Friday
• Budget approval needed from finance team

Looking forward to receiving your proposal. Let's schedule a follow-up in 2 weeks
to review progress and finalize the numbers.

Would any of these times work for a 30-minute call?
• Monday, March 27 at 10:00 AM EST
• Tuesday, March 28 at 2:00 PM EST
• Wednesday, March 29 at 11:00 AM EST

Best regards,
[Your name]
```

## Configuration File

Create `~/.config/sales-follow-up/config.yaml`:

```yaml
# Email settings
email:
  sender: "you@company.com"
  signature: |
    Best regards,
    John Smith
    Senior Account Executive
    Company Inc.

# Calendar settings
calendar:
  timezone: "America/New_York"
  buffer_minutes: 15  # Buffer between meetings
  working_hours:
    start: "09:00"
    end: "17:00"
  working_days: [1, 2, 3, 4, 5]  # Mon-Fri

# AI settings
ai:
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 500

# Follow-up rules
rules:
  auto_follow_up_after_days: 2
  suggest_next_meeting: true
  require_approval: true
  default_meeting_duration: 30

# CRM integration (optional)
crm:
  enabled: false
  type: "salesforce"  # or "hubspot", "pipedrive"
```

## Code Examples

### Python - Generate Follow-up

```python
from sales_follow_up import MeetingFollowUp, AIEmailGenerator

# Initialize
follow_up = MeetingFollowUp()
ai_generator = AIEmailGenerator()

# Get recent meeting
meeting = follow_up.get_meeting_by_name("Q1 Planning with Acme")

# Generate follow-up email
email = ai_generator.generate_follow_up(
    meeting_title=meeting.title,
    attendees=meeting.attendees,
    notes=meeting.notes,
    tone="professional"
)

print(f"Subject: {email.subject}")
print(f"Body:\n{email.body}")

# User approves
if input("Send? (y/n): ").lower() == 'y':
    follow_up.send_email(email)
    print("Email sent!")
```

### Python - Suggest Meeting Slots

```python
from sales_follow_up import CalendarManager

calendar = CalendarManager()

# Find available slots
slots = calendar.suggest_slots(
    attendees=["john@example.com", "jane@example.com"],
    duration_minutes=30,
    days_ahead=14,
    prefer_time="morning",  # or "afternoon", "any"
    count=5
)

for i, slot in enumerate(slots, 1):
    print(f"{i}. {slot.start.strftime('%A, %B %d at %I:%M %p')}")

# User selects
choice = int(input("Select slot (1-5): "))
selected = slots[choice - 1]

# Book meeting
calendar.book_meeting(
    title="Follow-up: Q1 Planning",
    start=selected.start,
    end=selected.end,
    attendees=["john@example.com"],
    description="Following up on our Q1 budget discussion"
)
```

### JavaScript/Node.js

```javascript
const { MeetingFollowUp, AIEmailGenerator } = require('./sales-follow-up');

async function autoFollowUp(meetingName) {
  const followUp = new MeetingFollowUp();
  const meeting = await followUp.getMeeting(meetingName);

  // Generate AI follow-up
  const email = await AIEmailGenerator.generate({
    meetingTitle: meeting.title,
    attendees: meeting.attendees,
    notes: meeting.notes
  });

  console.log(`\nDraft Email:\n${email.body}\n`);

  // Interactive approval
  const approved = await followUp.requestApproval('Send this email?');

  if (approved) {
    await followUp.sendEmail(email);
    console.log('Email sent!');

    // Suggest next meeting
    const slots = await followUp.suggestSlots(meeting.attendees, 30);
    const selected = await followUp.selectSlot(slots);
    await followUp.bookMeeting(selected);
  }
}
```

## Approval Workflow

Human-in-the-loop approval for critical actions:

```
┌─────────────────────────────────────┐
│  1. Detect completed meeting        │
│     (from Google Calendar)          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  2. Extract meeting notes & context │
│     (from description/notes)        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  3. AI generates follow-up email    │
│     (using GPT-4)                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  4. HUMAN APPROVAL REQUIRED         │
│     [Show draft, await confirmation]│
└──────────────┬──────────────────────┘
               │
         ┌─────┴─────┐
         │           │
       Approve    Reject/Edit
         │           │
         ▼           ▼
   ┌─────────┐  ┌──────────┐
   │  Send   │  │  Discard │
   │  Email  │  │  or Edit │
   └────┬────┘  └──────────┘
        │
        ▼
┌─────────────────────────────────────┐
│  5. Suggest next meeting slots      │
│     (check all calendars)           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  6. HUMAN APPROVAL REQUIRED         │
│     [Show slots, user selects]      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  7. Book meeting & send invite      │
└─────────────────────────────────────┘
```

## Best Practices

| Practice | Recommendation |
|----------|---------------|
| Approval Mode | Always require human approval for booking meetings |
| Follow-up Timing | Send within 24-48 hours of meeting |
| Meeting Notes | Include detailed notes for better AI context |
| Time Slots | Suggest 3-5 options to increase booking rate |
| Email Tone | Match tone to relationship (formal vs casual) |
| Calendar Buffer | Leave 15min buffer between meetings |

## Output Format

### Meeting Analysis

```markdown
## Meetings Requiring Follow-up

**Meeting:** Q1 Planning with Acme Corp
**Date:** March 15, 2024 2:00 PM
**Attendees:** John Doe (john@acme.com), Jane Smith
**Duration:** 30 minutes
**Status:** ⚠️ No follow-up sent

**Action Items:**
- John to send proposal by Friday
- Schedule follow-up in 2 weeks
- Review budget numbers

**Suggested Next Steps:**
1. Send follow-up email (draft available)
2. Book follow-up meeting for March 29-31
```

### Suggested Slots

```markdown
## Available Meeting Slots

**Requested:** 30-minute meeting with john@example.com, jane@example.com
**Date Range:** March 20-31, 2024

**Top 5 Recommended Times:**

1. ⭐ **Monday, March 27 at 10:00 AM EST**
   - All attendees available
   - Morning slot (preferred)
   - No conflicts

2. **Tuesday, March 28 at 2:00 PM EST**
   - All attendees available
   - Afternoon slot

3. **Wednesday, March 29 at 11:00 AM EST**
   - All attendees available
   - Late morning

4. **Thursday, March 30 at 9:00 AM EST**
   - All attendees available
   - Early slot

5. **Friday, March 31 at 3:00 PM EST**
   - All attendees available
   - End of week
```

## Integration with CRM

Optional integration with popular CRM systems:

```python
# config.yaml with CRM enabled
crm:
  enabled: true
  type: "salesforce"
  credentials: "~/.config/sales-follow-up/sf-creds.json"

# Auto-log follow-ups to CRM
python scripts/follow_up.py auto \
  --meeting "Acme Corp Demo" \
  --log-to-crm
```

## Scheduled Automation

Run as a cron job for daily follow-ups:

```bash
# crontab -e
# Run every day at 9 AM
0 9 * * * cd /path/to/scripts && python follow_up.py batch --date yesterday --require-approval
```

Or use the daemon mode:

```bash
# Start background service
python scripts/follow_up.py daemon --check-interval 3600

# Checks every hour for meetings needing follow-up
# Sends notifications when action required
```
