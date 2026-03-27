#!/usr/bin/env python3
"""
Email Marketing Automation - Campaign Manager

Features:
- Lead management from CSV/Google Sheets
- Template-based personalized emails
- Campaign sequences with delays
- Rate limiting and scheduling
- Engagement tracking
"""

import argparse
import csv
import json
import os
import smtplib
import sqlite3
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from string import Template
from typing import Optional
import re

# Optional imports
try:
    from jinja2 import Environment, FileSystemLoader
    HAS_JINJA = True
except ImportError:
    HAS_JINJA = False

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    import base64
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False


# Configuration
CONFIG_DIR = Path.home() / ".config" / "email-marketing"
DB_PATH = CONFIG_DIR / "campaigns.db"
TEMPLATES_DIR = CONFIG_DIR / "templates"
SCOPES = ['https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/spreadsheets.readonly']


@dataclass
class Lead:
    """Represents a marketing lead/contact."""
    email: str
    first_name: str = ""
    last_name: str = ""
    company: str = ""
    tags: list = field(default_factory=list)
    custom_fields: dict = field(default_factory=dict)
    status: str = "active"  # active, unsubscribed, bounced
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "company": self.company,
            "name": f"{self.first_name} {self.last_name}".strip(),
            **self.custom_fields
        }


@dataclass
class EmailMessage:
    """Represents an email to be sent."""
    to: str
    subject: str
    body_html: str
    body_text: str = ""
    from_addr: str = ""
    reply_to: str = ""
    campaign_id: str = ""
    lead_id: str = ""


class Database:
    """SQLite database for campaign tracking."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path))
        self._init_schema()

    def _init_schema(self):
        cursor = self.conn.cursor()

        # Leads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                first_name TEXT,
                last_name TEXT,
                company TEXT,
                tags TEXT,
                custom_fields TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Campaigns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                template TEXT,
                status TEXT DEFAULT 'draft',
                settings TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Email sends table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sends (
                id INTEGER PRIMARY KEY,
                campaign_id INTEGER,
                lead_id INTEGER,
                step INTEGER DEFAULT 1,
                status TEXT DEFAULT 'pending',
                sent_at TIMESTAMP,
                opened_at TIMESTAMP,
                clicked_at TIMESTAMP,
                replied_at TIMESTAMP,
                error TEXT,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            )
        ''')

        self.conn.commit()

    def add_lead(self, lead: Lead) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO leads
            (email, first_name, last_name, company, tags, custom_fields, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            lead.email,
            lead.first_name,
            lead.last_name,
            lead.company,
            json.dumps(lead.tags),
            json.dumps(lead.custom_fields),
            lead.status
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_leads(self, status: str = "active", tags: list = None) -> list[Lead]:
        cursor = self.conn.cursor()
        query = "SELECT * FROM leads WHERE status = ?"
        params = [status]

        cursor.execute(query, params)
        leads = []
        for row in cursor.fetchall():
            lead = Lead(
                email=row[1],
                first_name=row[2] or "",
                last_name=row[3] or "",
                company=row[4] or "",
                tags=json.loads(row[5] or "[]"),
                custom_fields=json.loads(row[6] or "{}"),
                status=row[7]
            )
            if tags is None or any(t in lead.tags for t in tags):
                leads.append(lead)
        return leads

    def create_campaign(self, name: str, template: str, settings: dict = None) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO campaigns (name, template, settings)
            VALUES (?, ?, ?)
        ''', (name, template, json.dumps(settings or {})))
        self.conn.commit()
        return cursor.lastrowid

    def record_send(self, campaign_id: int, lead_id: int, step: int = 1,
                    status: str = "sent", error: str = None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO sends (campaign_id, lead_id, step, status, sent_at, error)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (campaign_id, lead_id, step, status, datetime.now(), error))
        self.conn.commit()

    def get_campaign_stats(self, campaign_name: str) -> dict:
        cursor = self.conn.cursor()

        # Get campaign ID
        cursor.execute("SELECT id FROM campaigns WHERE name = ?", (campaign_name,))
        row = cursor.fetchone()
        if not row:
            return None
        campaign_id = row[0]

        # Get stats
        cursor.execute('''
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN status = 'sent' THEN 1 ELSE 0 END) as sent,
                SUM(CASE WHEN opened_at IS NOT NULL THEN 1 ELSE 0 END) as opened,
                SUM(CASE WHEN clicked_at IS NOT NULL THEN 1 ELSE 0 END) as clicked,
                SUM(CASE WHEN replied_at IS NOT NULL THEN 1 ELSE 0 END) as replied,
                SUM(CASE WHEN status = 'bounced' THEN 1 ELSE 0 END) as bounced,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed
            FROM sends WHERE campaign_id = ?
        ''', (campaign_id,))

        row = cursor.fetchone()
        return {
            "total": row[0],
            "sent": row[1],
            "opened": row[2],
            "clicked": row[3],
            "replied": row[4],
            "bounced": row[5],
            "failed": row[6]
        }


class TemplateEngine:
    """Handles email template rendering."""

    def __init__(self, templates_dir: Path = TEMPLATES_DIR):
        self.templates_dir = templates_dir
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        if HAS_JINJA:
            self.env = Environment(loader=FileSystemLoader(str(templates_dir)))

    def render(self, template_name: str, variables: dict) -> tuple[str, str]:
        """Render template and return (subject, body_html)."""
        template_path = self.templates_dir / template_name

        if not template_path.exists():
            # Check if it's inline content
            if "<" in template_name or "{{" in template_name:
                content = template_name
            else:
                raise FileNotFoundError(f"Template not found: {template_path}")
        else:
            content = template_path.read_text()

        # Extract subject from first line if present
        subject = ""
        lines = content.strip().split('\n')
        if lines[0].lower().startswith('subject:'):
            subject = lines[0].split(':', 1)[1].strip()
            content = '\n'.join(lines[1:]).strip()

        # Render with Jinja2 or basic substitution
        if HAS_JINJA:
            from jinja2 import Template as J2Template
            template = J2Template(content)
            body = template.render(**variables)
            if subject:
                subject_tmpl = J2Template(subject)
                subject = subject_tmpl.render(**variables)
        else:
            # Basic Python string Template
            template = Template(content)
            body = template.safe_substitute(variables)
            if subject:
                subject_tmpl = Template(subject)
                subject = subject_tmpl.safe_substitute(variables)

        return subject, body


class SMTPSender:
    """Send emails via SMTP."""

    def __init__(self):
        self.host = os.environ.get('EMAIL_SMTP_HOST', 'smtp.gmail.com')
        self.port = int(os.environ.get('EMAIL_SMTP_PORT', '587'))
        self.username = os.environ.get('EMAIL_SENDER', '')
        self.password = os.environ.get('EMAIL_APP_PASSWORD', '')

    def send(self, message: EmailMessage) -> bool:
        """Send an email via SMTP."""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = message.subject
        msg['From'] = message.from_addr or self.username
        msg['To'] = message.to

        if message.reply_to:
            msg['Reply-To'] = message.reply_to

        # Add text and HTML parts
        if message.body_text:
            msg.attach(MIMEText(message.body_text, 'plain'))
        msg.attach(MIMEText(message.body_html, 'html'))

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"SMTP Error: {e}")
            return False


class GmailSender:
    """Send emails via Gmail API."""

    def __init__(self):
        if not HAS_GOOGLE:
            raise ImportError("Google API libraries not installed. Run: pip install google-auth google-auth-oauthlib google-api-python-client")

        self.creds = self._get_credentials()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def _get_credentials(self):
        creds = None
        token_path = CONFIG_DIR / "token.json"
        creds_path = Path(os.environ.get('GOOGLE_CREDENTIALS_PATH', CONFIG_DIR / "credentials.json"))

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
                creds = flow.run_local_server(port=0)

            token_path.write_text(creds.to_json())

        return creds

    def send(self, message: EmailMessage) -> bool:
        """Send an email via Gmail API."""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = message.subject
        msg['From'] = message.from_addr or os.environ.get('EMAIL_SENDER', '')
        msg['To'] = message.to

        if message.reply_to:
            msg['Reply-To'] = message.reply_to

        if message.body_text:
            msg.attach(MIMEText(message.body_text, 'plain'))
        msg.attach(MIMEText(message.body_html, 'html'))

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

        try:
            self.service.users().messages().send(
                userId='me',
                body={'raw': raw}
            ).execute()
            return True
        except Exception as e:
            print(f"Gmail API Error: {e}")
            return False


class Campaign:
    """Manages email campaigns."""

    def __init__(self, name: str, template: str = None,
                 sender: str = "smtp", rate_limit: int = 50):
        self.name = name
        self.template = template
        self.rate_limit = rate_limit  # emails per hour
        self.db = Database()
        self.template_engine = TemplateEngine()

        # Initialize sender
        if sender == "gmail":
            self.sender = GmailSender()
        else:
            self.sender = SMTPSender()

    def import_leads(self, source: str, sheet_id: str = None,
                     sheet_range: str = "A1:Z1000") -> int:
        """Import leads from CSV or Google Sheets."""
        leads = []

        if sheet_id and HAS_GOOGLE:
            # Import from Google Sheets
            creds = GmailSender()._get_credentials()
            service = build('sheets', 'v4', credentials=creds)

            result = service.spreadsheets().values().get(
                spreadsheetId=sheet_id,
                range=sheet_range
            ).execute()

            rows = result.get('values', [])
            if rows:
                headers = [h.lower().replace(' ', '_') for h in rows[0]]
                for row in rows[1:]:
                    data = dict(zip(headers, row + [''] * (len(headers) - len(row))))
                    lead = Lead(
                        email=data.get('email', ''),
                        first_name=data.get('first_name', data.get('name', '').split()[0] if data.get('name') else ''),
                        last_name=data.get('last_name', ' '.join(data.get('name', '').split()[1:]) if data.get('name') else ''),
                        company=data.get('company', ''),
                        tags=data.get('tags', '').split(',') if data.get('tags') else []
                    )
                    if lead.email:
                        leads.append(lead)
        else:
            # Import from CSV
            with open(source, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Normalize keys
                    row = {k.lower().replace(' ', '_'): v for k, v in row.items()}
                    lead = Lead(
                        email=row.get('email', ''),
                        first_name=row.get('first_name', row.get('name', '').split()[0] if row.get('name') else ''),
                        last_name=row.get('last_name', ''),
                        company=row.get('company', ''),
                        tags=row.get('tags', '').split(',') if row.get('tags') else []
                    )
                    if lead.email:
                        leads.append(lead)

        # Save to database
        for lead in leads:
            self.db.add_lead(lead)

        print(f"Imported {len(leads)} leads")
        return len(leads)

    def preview(self, limit: int = 5) -> list[dict]:
        """Preview emails that would be sent."""
        leads = self.db.get_leads()[:limit]
        previews = []

        for lead in leads:
            subject, body = self.template_engine.render(
                self.template,
                lead.to_dict()
            )
            previews.append({
                "to": lead.email,
                "subject": subject,
                "body_preview": body[:200] + "..." if len(body) > 200 else body
            })

        return previews

    def run(self, dry_run: bool = False, tags: list = None) -> dict:
        """Run the campaign, sending emails to all active leads."""
        leads = self.db.get_leads(tags=tags)

        # Get or create campaign in DB
        try:
            campaign_id = self.db.create_campaign(self.name, self.template)
        except sqlite3.IntegrityError:
            # Campaign exists, get its ID
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT id FROM campaigns WHERE name = ?", (self.name,))
            campaign_id = cursor.fetchone()[0]

        stats = {"sent": 0, "failed": 0, "skipped": 0}
        delay = 3600 / self.rate_limit  # seconds between emails

        print(f"Starting campaign '{self.name}' with {len(leads)} leads")
        print(f"Rate limit: {self.rate_limit}/hour ({delay:.1f}s between emails)")

        if dry_run:
            print("\n[DRY RUN - No emails will be sent]\n")

        for i, lead in enumerate(leads):
            try:
                subject, body = self.template_engine.render(
                    self.template,
                    lead.to_dict()
                )

                message = EmailMessage(
                    to=lead.email,
                    subject=subject,
                    body_html=body,
                    campaign_id=str(campaign_id)
                )

                if dry_run:
                    print(f"[{i+1}/{len(leads)}] Would send to: {lead.email}")
                    print(f"    Subject: {subject}")
                    stats["sent"] += 1
                else:
                    print(f"[{i+1}/{len(leads)}] Sending to: {lead.email}...", end=" ")

                    if self.sender.send(message):
                        self.db.record_send(campaign_id, i, status="sent")
                        print("OK")
                        stats["sent"] += 1
                    else:
                        self.db.record_send(campaign_id, i, status="failed")
                        print("FAILED")
                        stats["failed"] += 1

                    # Rate limiting
                    if i < len(leads) - 1:
                        time.sleep(delay)

            except Exception as e:
                print(f"Error with {lead.email}: {e}")
                stats["failed"] += 1

        print(f"\nCampaign complete: {stats['sent']} sent, {stats['failed']} failed")
        return stats

    def stats(self) -> dict:
        """Get campaign statistics."""
        return self.db.get_campaign_stats(self.name)


def main():
    parser = argparse.ArgumentParser(description="Email Marketing Automation")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Import leads
    import_parser = subparsers.add_parser("import-leads", help="Import leads from CSV or Google Sheets")
    import_parser.add_argument("source", help="CSV file path")
    import_parser.add_argument("--sheets", help="Google Sheets ID (instead of CSV)")
    import_parser.add_argument("--range", default="A1:Z1000", help="Sheet range")

    # Create campaign
    create_parser = subparsers.add_parser("create", help="Create a new campaign")
    create_parser.add_argument("name", help="Campaign name")
    create_parser.add_argument("--template", required=True, help="Template file name")
    create_parser.add_argument("--delay", default="0", help="Delay between steps (e.g., 2d, 1h)")

    # Send single email
    send_parser = subparsers.add_parser("send", help="Send a single email")
    send_parser.add_argument("--to", required=True, help="Recipient email")
    send_parser.add_argument("--template", required=True, help="Template file name")
    send_parser.add_argument("--vars", default="{}", help="Variables as JSON")
    send_parser.add_argument("--sender", choices=["smtp", "gmail"], default="smtp")

    # Run campaign
    run_parser = subparsers.add_parser("run", help="Run a campaign")
    run_parser.add_argument("name", help="Campaign name")
    run_parser.add_argument("--template", help="Template file (or use saved)")
    run_parser.add_argument("--dry-run", action="store_true", help="Preview without sending")
    run_parser.add_argument("--rate-limit", type=int, default=50, help="Emails per hour")
    run_parser.add_argument("--sender", choices=["smtp", "gmail"], default="smtp")
    run_parser.add_argument("--tags", help="Only send to leads with these tags (comma-separated)")

    # Campaign stats
    stats_parser = subparsers.add_parser("stats", help="View campaign statistics")
    stats_parser.add_argument("name", help="Campaign name")

    # Export stats
    export_parser = subparsers.add_parser("export-stats", help="Export campaign stats to CSV")
    export_parser.add_argument("name", help="Campaign name")
    export_parser.add_argument("-o", "--output", default="stats.csv", help="Output file")

    # List campaigns
    subparsers.add_parser("list", help="List all campaigns")

    args = parser.parse_args()

    if args.command == "import-leads":
        campaign = Campaign("default")
        campaign.import_leads(args.source, args.sheets, args.range)

    elif args.command == "create":
        db = Database()
        db.create_campaign(args.name, args.template)
        print(f"Created campaign: {args.name}")

    elif args.command == "send":
        variables = json.loads(args.vars)
        template_engine = TemplateEngine()
        subject, body = template_engine.render(args.template, variables)

        if args.sender == "gmail":
            sender = GmailSender()
        else:
            sender = SMTPSender()

        message = EmailMessage(
            to=args.to,
            subject=subject,
            body_html=body
        )

        if sender.send(message):
            print(f"Email sent to {args.to}")
        else:
            print("Failed to send email")

    elif args.command == "run":
        tags = args.tags.split(',') if args.tags else None
        campaign = Campaign(
            args.name,
            template=args.template,
            sender=args.sender,
            rate_limit=args.rate_limit
        )
        campaign.run(dry_run=args.dry_run, tags=tags)

    elif args.command == "stats":
        campaign = Campaign(args.name)
        stats = campaign.stats()

        if stats:
            print(f"\n## Campaign: {args.name}\n")
            print(f"| Metric | Count | Rate |")
            print(f"|--------|-------|------|")

            total = stats['total'] or 1
            for metric in ['sent', 'opened', 'clicked', 'replied', 'bounced', 'failed']:
                count = stats[metric] or 0
                rate = (count / total) * 100
                print(f"| {metric.capitalize()} | {count} | {rate:.1f}% |")
        else:
            print(f"Campaign '{args.name}' not found")

    elif args.command == "list":
        db = Database()
        cursor = db.conn.cursor()
        cursor.execute("SELECT name, status, created_at FROM campaigns")

        print("\n| Campaign | Status | Created |")
        print("|----------|--------|---------|")
        for row in cursor.fetchall():
            print(f"| {row[0]} | {row[1]} | {row[2]} |")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
