#!/usr/bin/env python3
"""
Sales Meeting Follow-Up Automation

Features:
- Google Calendar integration for meeting tracking
- AI-powered follow-up email generation (OpenAI GPT-4)
- Smart meeting slot suggestions based on availability
- Human approval workflow for booking/sending
- Meeting notes extraction and action item tracking
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import yaml

# Optional imports
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    import base64
    from email.mime.text import MIMEText
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Configuration
CONFIG_DIR = Path.home() / ".config" / "sales-follow-up"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/gmail.send'
]


@dataclass
class Meeting:
    """Represents a calendar meeting."""
    id: str
    title: str
    start: datetime
    end: datetime
    attendees: list[str] = field(default_factory=list)
    organizer: str = ""
    notes: str = ""
    location: str = ""
    status: str = "confirmed"

    @property
    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() / 60)


@dataclass
class TimeSlot:
    """Represents an available time slot."""
    start: datetime
    end: datetime
    score: float = 0.0  # Higher is better
    reason: str = ""


@dataclass
class Email:
    """Represents an email message."""
    to: list[str]
    subject: str
    body: str
    cc: list[str] = field(default_factory=list)
    reply_to: str = ""


class Config:
    """Application configuration."""

    DEFAULT_CONFIG = {
        'email': {
            'sender': os.environ.get('EMAIL_SENDER', ''),
            'signature': ''
        },
        'calendar': {
            'timezone': os.environ.get('TIMEZONE', 'UTC'),
            'buffer_minutes': 15,
            'working_hours': {'start': '09:00', 'end': '17:00'},
            'working_days': [1, 2, 3, 4, 5]
        },
        'ai': {
            'model': 'gpt-4',
            'temperature': 0.7,
            'max_tokens': 500
        },
        'rules': {
            'auto_follow_up_after_days': 2,
            'suggest_next_meeting': True,
            'require_approval': True,
            'default_meeting_duration': 30
        }
    }

    def __init__(self):
        self.data = self.load()

    def load(self) -> dict:
        """Load configuration from file."""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                return yaml.safe_load(f) or self.DEFAULT_CONFIG
        else:
            # Create default config
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                yaml.dump(self.DEFAULT_CONFIG, f, default_flow_style=False)
            return self.DEFAULT_CONFIG

    def get(self, key: str, default=None):
        """Get nested config value using dot notation."""
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value


class GoogleCalendarManager:
    """Manages Google Calendar operations."""

    def __init__(self):
        if not HAS_GOOGLE:
            raise ImportError("Google API libraries required. Run: pip install google-auth google-auth-oauthlib google-api-python-client")

        self.config = Config()
        self.creds = self._get_credentials()
        self.calendar_service = build('calendar', 'v3', credentials=self.creds)
        self.gmail_service = build('gmail', 'v1', credentials=self.creds)

    def _get_credentials(self):
        """Authenticate and get Google API credentials."""
        creds = None
        token_path = CONFIG_DIR / "token.json"
        creds_path = Path(os.environ.get('GOOGLE_CREDENTIALS_PATH',
                                        CONFIG_DIR / "credentials.json"))

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not creds_path.exists():
                    print(f"Error: credentials.json not found at {creds_path}")
                    print("Download from Google Cloud Console and place it there")
                    sys.exit(1)

                flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
                creds = flow.run_local_server(port=0)

            token_path.write_text(creds.to_json())

        return creds

    def get_recent_meetings(self, days: int = 7) -> list[Meeting]:
        """Get meetings from the last N days."""
        now = datetime.utcnow()
        time_min = (now - timedelta(days=days)).isoformat() + 'Z'
        time_max = now.isoformat() + 'Z'

        events_result = self.calendar_service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        meetings = []

        for event in events:
            if 'dateTime' in event.get('start', {}):
                meeting = self._parse_event(event)
                meetings.append(meeting)

        return meetings

    def get_meeting_by_name(self, name: str) -> Optional[Meeting]:
        """Find a meeting by name/title."""
        meetings = self.get_recent_meetings(days=30)
        for meeting in meetings:
            if name.lower() in meeting.title.lower():
                return meeting
        return None

    def _parse_event(self, event: dict) -> Meeting:
        """Parse Google Calendar event to Meeting object."""
        start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
        end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))

        attendees = []
        for attendee in event.get('attendees', []):
            attendees.append(attendee.get('email', ''))

        return Meeting(
            id=event['id'],
            title=event.get('summary', 'No Title'),
            start=start,
            end=end,
            attendees=attendees,
            organizer=event.get('organizer', {}).get('email', ''),
            notes=event.get('description', ''),
            location=event.get('location', '')
        )

    def suggest_slots(self, attendees: list[str], duration_minutes: int,
                     days_ahead: int = 14, prefer_time: str = "any",
                     count: int = 5) -> list[TimeSlot]:
        """Suggest available meeting slots."""
        now = datetime.utcnow()
        time_min = now.isoformat() + 'Z'
        time_max = (now + timedelta(days=days_ahead)).isoformat() + 'Z'

        # Get free/busy information for all attendees
        body = {
            "timeMin": time_min,
            "timeMax": time_max,
            "items": [{"id": email} for email in attendees + ['primary']]
        }

        freebusy = self.calendar_service.freebusy().query(body=body).execute()
        calendars = freebusy.get('calendars', {})

        # Find available slots
        working_hours = self.config.get('calendar.working_hours', {'start': '09:00', 'end': '17:00'})
        working_days = self.config.get('calendar.working_days', [1, 2, 3, 4, 5])
        buffer_minutes = self.config.get('calendar.buffer_minutes', 15)

        slots = []
        current = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        end_date = current + timedelta(days=days_ahead)

        while current < end_date:
            # Skip non-working days
            if current.isoweekday() not in working_days:
                current += timedelta(days=1)
                continue

            # Parse working hours
            start_hour, start_min = map(int, working_hours['start'].split(':'))
            end_hour, end_min = map(int, working_hours['end'].split(':'))

            day_start = current.replace(hour=start_hour, minute=start_min)
            day_end = current.replace(hour=end_hour, minute=end_min)

            # Check every 30-minute slot
            slot_start = day_start
            while slot_start + timedelta(minutes=duration_minutes + buffer_minutes) <= day_end:
                slot_end = slot_start + timedelta(minutes=duration_minutes)

                # Check if all attendees are free
                is_free = True
                for calendar_id, calendar_data in calendars.items():
                    busy_times = calendar_data.get('busy', [])
                    for busy in busy_times:
                        busy_start = datetime.fromisoformat(busy['start'].replace('Z', '+00:00'))
                        busy_end = datetime.fromisoformat(busy['end'].replace('Z', '+00:00'))

                        # Check overlap with buffer
                        if not (slot_end.replace(tzinfo=None) + timedelta(minutes=buffer_minutes) <= busy_start.replace(tzinfo=None) or
                                slot_start.replace(tzinfo=None) >= busy_end.replace(tzinfo=None)):
                            is_free = False
                            break

                    if not is_free:
                        break

                if is_free:
                    # Score the slot
                    score = self._score_slot(slot_start, prefer_time)
                    reason = self._slot_reason(slot_start, prefer_time)

                    slots.append(TimeSlot(
                        start=slot_start,
                        end=slot_end,
                        score=score,
                        reason=reason
                    ))

                slot_start += timedelta(minutes=30)

            current += timedelta(days=1)

        # Sort by score and return top N
        slots.sort(key=lambda x: x.score, reverse=True)
        return slots[:count]

    def _score_slot(self, slot_time: datetime, prefer: str) -> float:
        """Score a time slot based on preferences."""
        score = 100.0
        hour = slot_time.hour

        # Time of day preference
        if prefer == "morning" and 9 <= hour < 12:
            score += 20
        elif prefer == "afternoon" and 13 <= hour < 17:
            score += 20
        elif prefer == "any":
            score += 10

        # Prefer mid-week
        weekday = slot_time.isoweekday()
        if weekday in [2, 3, 4]:  # Tue, Wed, Thu
            score += 15
        elif weekday in [1, 5]:  # Mon, Fri
            score += 5

        # Prefer whole/half hours
        if slot_time.minute == 0:
            score += 10
        elif slot_time.minute == 30:
            score += 5

        # Slight preference for sooner rather than later
        days_out = (slot_time.date() - datetime.now().date()).days
        score -= days_out * 0.5

        return score

    def _slot_reason(self, slot_time: datetime, prefer: str) -> str:
        """Generate reason text for slot selection."""
        reasons = []

        hour = slot_time.hour
        if prefer == "morning" and 9 <= hour < 12:
            reasons.append("Morning slot (preferred)")
        elif prefer == "afternoon" and 13 <= hour < 17:
            reasons.append("Afternoon slot (preferred)")

        weekday = slot_time.isoweekday()
        if weekday in [2, 3, 4]:
            reasons.append("Mid-week")

        if slot_time.minute == 0:
            reasons.append("On the hour")

        return ", ".join(reasons) if reasons else "Available"

    def book_meeting(self, title: str, start: datetime, end: datetime,
                    attendees: list[str], description: str = "") -> str:
        """Book a meeting on the calendar."""
        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start.isoformat(),
                'timeZone': self.config.get('calendar.timezone', 'UTC')
            },
            'end': {
                'dateTime': end.isoformat(),
                'timeZone': self.config.get('calendar.timezone', 'UTC')
            },
            'attendees': [{'email': email} for email in attendees],
            'reminders': {
                'useDefault': True
            }
        }

        created_event = self.calendar_service.events().insert(
            calendarId='primary',
            body=event,
            sendUpdates='all'
        ).execute()

        return created_event['id']

    def send_email(self, email: Email) -> bool:
        """Send an email via Gmail API."""
        message = MIMEText(email.body)
        message['to'] = ', '.join(email.to)
        message['subject'] = email.subject
        message['from'] = self.config.get('email.sender', '')

        if email.cc:
            message['cc'] = ', '.join(email.cc)
        if email.reply_to:
            message['reply-to'] = email.reply_to

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        try:
            self.gmail_service.users().messages().send(
                userId='me',
                body={'raw': raw}
            ).execute()
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False


class AIEmailGenerator:
    """Generate follow-up emails using AI."""

    def __init__(self):
        if not HAS_OPENAI:
            raise ImportError("OpenAI library required. Run: pip install openai")

        self.config = Config()
        openai.api_key = os.environ.get('OPENAI_API_KEY')

        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

    def generate_follow_up(self, meeting_title: str, attendees: list[str],
                          notes: str = "", tone: str = "professional",
                          suggest_next_meeting: bool = True) -> Email:
        """Generate a follow-up email using GPT-4."""

        prompt = f"""Generate a professional follow-up email for a sales meeting.

Meeting Title: {meeting_title}
Attendees: {', '.join(attendees)}
Meeting Notes: {notes if notes else 'No notes provided'}
Tone: {tone}

Requirements:
- Thank attendees for their time
- Summarize key discussion points and action items
- Be concise and professional
- Include next steps
{'- Suggest scheduling a follow-up meeting' if suggest_next_meeting else ''}

Format:
Subject: [email subject]

[email body]
"""

        try:
            response = openai.ChatCompletion.create(
                model=self.config.get('ai.model', 'gpt-4'),
                messages=[
                    {"role": "system", "content": "You are a helpful sales assistant that writes professional follow-up emails."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.get('ai.temperature', 0.7),
                max_tokens=self.config.get('ai.max_tokens', 500)
            )

            content = response.choices[0].message.content.strip()

            # Parse subject and body
            lines = content.split('\n')
            subject = ""
            body_lines = []

            for line in lines:
                if line.lower().startswith('subject:'):
                    subject = line.split(':', 1)[1].strip()
                elif line.strip():
                    body_lines.append(line)

            body = '\n'.join(body_lines).strip()

            # Add signature
            signature = self.config.get('email.signature', '')
            if signature:
                body += f"\n\n{signature}"

            return Email(
                to=attendees,
                subject=subject or f"Following up on {meeting_title}",
                body=body
            )

        except Exception as e:
            print(f"Error generating email: {e}")
            raise


class MeetingFollowUp:
    """Main follow-up orchestration."""

    def __init__(self):
        self.config = Config()
        self.calendar = GoogleCalendarManager()
        self.ai = AIEmailGenerator()

    def analyze_meetings(self, days: int = 7) -> list[Meeting]:
        """Find meetings that need follow-up."""
        meetings = self.calendar.get_recent_meetings(days)

        # Filter meetings that likely need follow-up
        needs_followup = []
        for meeting in meetings:
            # Skip if only 1 attendee (no external people)
            if len(meeting.attendees) <= 1:
                continue

            # Skip if in the future
            if meeting.start > datetime.now():
                continue

            # Skip all-day events or very short meetings
            if meeting.duration_minutes < 15:
                continue

            needs_followup.append(meeting)

        return needs_followup

    def request_approval(self, prompt: str, options: list = None) -> str:
        """Request human approval/input."""
        print(f"\n{prompt}")

        if options:
            for i, opt in enumerate(options, 1):
                print(f"  {i}. {opt}")
            choice = input("\nYour choice: ").strip()
            return choice
        else:
            response = input("(y/n): ").strip().lower()
            return response == 'y'

    def auto_follow_up(self, meeting_name: str, interactive: bool = True):
        """Complete follow-up workflow for a meeting."""
        # 1. Find meeting
        print(f"Looking for meeting: {meeting_name}")
        meeting = self.calendar.get_meeting_by_name(meeting_name)

        if not meeting:
            print(f"Meeting not found: {meeting_name}")
            return

        print(f"\nFound: {meeting.title}")
        print(f"Date: {meeting.start.strftime('%B %d, %Y %I:%M %p')}")
        print(f"Attendees: {', '.join(meeting.attendees)}")
        print(f"Duration: {meeting.duration_minutes} minutes")

        # 2. Generate follow-up email
        print("\nGenerating follow-up email...")
        email = self.ai.generate_follow_up(
            meeting_title=meeting.title,
            attendees=meeting.attendees,
            notes=meeting.notes,
            suggest_next_meeting=self.config.get('rules.suggest_next_meeting', True)
        )

        # 3. Show draft and request approval
        print("\n" + "="*60)
        print("DRAFT EMAIL")
        print("="*60)
        print(f"To: {', '.join(email.to)}")
        print(f"Subject: {email.subject}")
        print(f"\n{email.body}")
        print("="*60)

        if interactive:
            if not self.request_approval("\nSend this email?"):
                print("Email cancelled")
                return

        # 4. Send email
        print("\nSending email...")
        if self.calendar.send_email(email):
            print("Email sent successfully!")
        else:
            print("Failed to send email")
            return

        # 5. Suggest next meeting
        if self.config.get('rules.suggest_next_meeting', True):
            print("\nFinding available meeting slots...")

            duration = self.config.get('rules.default_meeting_duration', 30)
            slots = self.calendar.suggest_slots(
                attendees=meeting.attendees,
                duration_minutes=duration,
                days_ahead=14,
                count=5
            )

            if slots:
                print("\n" + "="*60)
                print("SUGGESTED MEETING TIMES")
                print("="*60)

                slot_descriptions = []
                for i, slot in enumerate(slots, 1):
                    desc = slot.start.strftime('%A, %B %d at %I:%M %p')
                    if slot.reason:
                        desc += f" ({slot.reason})"
                    print(f"{i}. {desc}")
                    slot_descriptions.append(desc)

                if interactive:
                    choice = self.request_approval(
                        "\nBook a follow-up meeting? (Enter number or 'n' to skip)",
                        slot_descriptions
                    )

                    if choice.isdigit() and 1 <= int(choice) <= len(slots):
                        selected_slot = slots[int(choice) - 1]

                        meeting_id = self.calendar.book_meeting(
                            title=f"Follow-up: {meeting.title}",
                            start=selected_slot.start,
                            end=selected_slot.end,
                            attendees=meeting.attendees,
                            description=f"Following up on our previous discussion"
                        )

                        print(f"\nMeeting booked! ID: {meeting_id}")
                    else:
                        print("Meeting booking skipped")
            else:
                print("No available slots found")


def main():
    parser = argparse.ArgumentParser(description="Sales Meeting Follow-Up Automation")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Analyze meetings
    analyze_parser = subparsers.add_parser("analyze", help="Analyze meetings needing follow-up")
    analyze_parser.add_argument("--days", type=int, default=7, help="Look back N days")

    # Draft email
    draft_parser = subparsers.add_parser("draft", help="Draft follow-up email")
    draft_parser.add_argument("meeting", help="Meeting name/title")
    draft_parser.add_argument("--notes", default="", help="Meeting notes")
    draft_parser.add_argument("--tone", default="professional", help="Email tone")

    # Suggest slots
    suggest_parser = subparsers.add_parser("suggest-slots", help="Suggest meeting times")
    suggest_parser.add_argument("--attendees", required=True, help="Comma-separated emails")
    suggest_parser.add_argument("--duration", type=int, default=30, help="Meeting duration (minutes)")
    suggest_parser.add_argument("--days-ahead", type=int, default=14, help="Search N days ahead")
    suggest_parser.add_argument("--prefer-morning", action="store_true", help="Prefer morning slots")
    suggest_parser.add_argument("--prefer-afternoon", action="store_true", help="Prefer afternoon slots")

    # Book meeting
    book_parser = subparsers.add_parser("book", help="Book a meeting")
    book_parser.add_argument("--attendees", required=True, help="Comma-separated emails")
    book_parser.add_argument("--subject", required=True, help="Meeting subject")
    book_parser.add_argument("--duration", type=int, default=30, help="Duration (minutes)")
    book_parser.add_argument("--auto-suggest", action="store_true", help="Auto-suggest slots first")

    # Auto workflow
    auto_parser = subparsers.add_parser("auto", help="Complete follow-up workflow")
    auto_parser.add_argument("--meeting", required=True, help="Meeting name")
    auto_parser.add_argument("--suggest-next-meeting", action="store_true", default=True)
    auto_parser.add_argument("--approve-mode", choices=["interactive", "auto"], default="interactive")

    # Batch process
    batch_parser = subparsers.add_parser("batch", help="Process multiple meetings")
    batch_parser.add_argument("--date", default="yesterday", help="Date to process")
    batch_parser.add_argument("--require-approval", action="store_true", default=True)

    args = parser.parse_args()

    try:
        if args.command == "analyze":
            follow_up = MeetingFollowUp()
            meetings = follow_up.analyze_meetings(args.days)

            print(f"\n## Meetings Requiring Follow-up ({len(meetings)})\n")

            for meeting in meetings:
                print(f"**Meeting:** {meeting.title}")
                print(f"**Date:** {meeting.start.strftime('%B %d, %Y %I:%M %p')}")
                print(f"**Attendees:** {', '.join(meeting.attendees)}")
                print(f"**Duration:** {meeting.duration_minutes} minutes")
                if meeting.notes:
                    print(f"**Notes:** {meeting.notes[:100]}...")
                print()

        elif args.command == "draft":
            follow_up = MeetingFollowUp()
            meeting = follow_up.calendar.get_meeting_by_name(args.meeting)

            if not meeting:
                print(f"Meeting not found: {args.meeting}")
                return

            email = follow_up.ai.generate_follow_up(
                meeting_title=meeting.title,
                attendees=meeting.attendees,
                notes=args.notes or meeting.notes,
                tone=args.tone
            )

            print(f"\nSubject: {email.subject}\n")
            print(email.body)

        elif args.command == "suggest-slots":
            calendar = GoogleCalendarManager()
            attendees = [a.strip() for a in args.attendees.split(',')]

            prefer = "any"
            if args.prefer_morning:
                prefer = "morning"
            elif args.prefer_afternoon:
                prefer = "afternoon"

            slots = calendar.suggest_slots(
                attendees=attendees,
                duration_minutes=args.duration,
                days_ahead=args.days_ahead,
                prefer_time=prefer
            )

            print(f"\n## Available Meeting Slots\n")
            for i, slot in enumerate(slots, 1):
                desc = slot.start.strftime('%A, %B %d at %I:%M %p')
                if slot.reason:
                    desc += f" ({slot.reason})"
                print(f"{i}. {desc}")

        elif args.command == "auto":
            follow_up = MeetingFollowUp()
            follow_up.auto_follow_up(
                args.meeting,
                interactive=(args.approve_mode == "interactive")
            )

        elif args.command == "batch":
            follow_up = MeetingFollowUp()
            meetings = follow_up.analyze_meetings(days=1)

            print(f"Found {len(meetings)} meetings to process\n")

            for meeting in meetings:
                print(f"\n{'='*60}")
                print(f"Meeting: {meeting.title}")
                print(f"{'='*60}")

                if args.require_approval:
                    if not follow_up.request_approval("Process this meeting?"):
                        continue

                follow_up.auto_follow_up(meeting.title, interactive=args.require_approval)

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
