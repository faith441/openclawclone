#!/usr/bin/env python3
"""
Email Automation Agent

Simple email sending with:
- Send single emails
- Send bulk emails from CSV
- Template support
- Attachment handling
- Only requires SMTP credentials (no API keys needed!)
"""

import argparse
import json
import os
import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime

class EmailAgent:
    def __init__(self):
        self.smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
        self.smtp_user = os.environ.get('SMTP_USER')
        self.smtp_pass = os.environ.get('SMTP_PASS')
        self.from_email = os.environ.get('FROM_EMAIL', self.smtp_user)

        if not self.smtp_user or not self.smtp_pass:
            print("⚠️  SMTP credentials not configured")
            print("Set: SMTP_USER, SMTP_PASS")
            print("Optional: SMTP_HOST (default: smtp.gmail.com), SMTP_PORT (default: 587)")

    def send_email(self, to_email: str, subject: str, body: str, attachments: list = None, html: bool = False) -> bool:
        """Send a single email."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email

            # Add body
            content_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, content_type))

            # Add attachments
            if attachments:
                for file_path in attachments:
                    if Path(file_path).exists():
                        with open(file_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', f'attachment; filename={Path(file_path).name}')
                            msg.attach(part)

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)

            print(f"✓ Email sent to: {to_email}")
            return True

        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")
            return False

    def send_bulk_emails(self, csv_file: str, subject_template: str, body_template: str) -> dict:
        """Send bulk emails from CSV file."""
        results = {"sent": 0, "failed": 0, "emails": []}

        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Replace template variables
                    subject = subject_template
                    body = body_template

                    for key, value in row.items():
                        subject = subject.replace(f"{{{{{key}}}}}", value)
                        body = body.replace(f"{{{{{key}}}}}", value)

                    # Send email
                    if self.send_email(row.get('email', ''), subject, body):
                        results['sent'] += 1
                        results['emails'].append({"email": row.get('email'), "status": "sent"})
                    else:
                        results['failed'] += 1
                        results['emails'].append({"email": row.get('email'), "status": "failed"})

        except Exception as e:
            print(f"❌ Bulk email failed: {e}")

        return results

def main():
    parser = argparse.ArgumentParser(description="Email Automation Agent")
    parser.add_argument('--to', help='Recipient email address')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--body', help='Email body text')
    parser.add_argument('--bulk', help='CSV file for bulk emails')
    parser.add_argument('--html', action='store_true', help='Send as HTML email')
    parser.add_argument('--attach', nargs='*', help='File attachments')

    args = parser.parse_args()

    agent = EmailAgent()

    if args.bulk:
        # Bulk email mode
        print(f"Sending bulk emails from: {args.bulk}")
        subject_template = args.subject or "Hello {{name}}"
        body_template = args.body or "Hi {{name}},\n\nThis is an automated email."

        results = agent.send_bulk_emails(args.bulk, subject_template, body_template)

        print(f"\n=== Bulk Email Results ===")
        print(f"Sent: {results['sent']}")
        print(f"Failed: {results['failed']}")
        print(json.dumps(results, indent=2))

    elif args.to and args.subject and args.body:
        # Single email mode
        success = agent.send_email(
            args.to,
            args.subject,
            args.body,
            args.attach,
            args.html
        )

        if success:
            print("\n✓ Email sent successfully!")
        else:
            print("\n❌ Email sending failed")

    else:
        print("Usage:")
        print("  Single email: --to EMAIL --subject SUBJECT --body BODY [--attach FILE ...]")
        print("  Bulk emails:  --bulk CSV_FILE [--subject TEMPLATE] [--body TEMPLATE]")

if __name__ == "__main__":
    main()
