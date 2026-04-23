#!/usr/bin/env python3
"""
SMS Notification Agent

Send SMS messages via Twilio:
- Send single SMS
- Send bulk SMS from CSV
- Delivery tracking
- Template support
- Easy setup with Twilio free trial ($15 credit)
"""

import argparse
import json
import os
import csv
from datetime import datetime
from pathlib import Path

class SMSAgent:
    def __init__(self):
        self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.from_number = os.environ.get('TWILIO_PHONE_NUMBER')

        self.has_twilio = False
        self.client = None

        if not all([self.account_sid, self.auth_token, self.from_number]):
            print("⚠️  Twilio credentials not configured")
            print("Set: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER")
            print("\nGet free trial at: https://www.twilio.com/try-twilio")
            print("Free trial includes $15 credit!")
        else:
            try:
                from twilio.rest import Client
                self.client = Client(self.account_sid, self.auth_token)
                self.has_twilio = True
            except ImportError:
                print("⚠️  twilio library not installed. Run: pip install twilio")

    def send_sms(self, to_number: str, message: str) -> dict:
        """Send a single SMS message."""
        if not self.has_twilio:
            return {"status": "failed", "error": "Twilio not configured"}

        try:
            # Send SMS
            response = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )

            result = {
                "status": "sent",
                "to": to_number,
                "sid": response.sid,
                "price": response.price,
                "timestamp": datetime.now().isoformat()
            }

            print(f"✓ SMS sent to: {to_number}")
            print(f"✓ Message SID: {response.sid}")
            if response.price:
                print(f"✓ Cost: ${abs(float(response.price)):.4f}")

            return result

        except Exception as e:
            print(f"❌ Failed to send SMS to {to_number}: {e}")
            return {"status": "failed", "to": to_number, "error": str(e)}

    def send_bulk_sms(self, csv_file: str, message_template: str) -> dict:
        """Send bulk SMS from CSV file."""
        results = {"sent": 0, "failed": 0, "messages": [], "total_cost": 0.0}

        if not self.has_twilio:
            print("❌ Twilio not configured")
            return results

        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Replace template variables
                    message = message_template
                    for key, value in row.items():
                        message = message.replace(f"{{{{{key}}}}}", value)

                    # Get phone number
                    phone = row.get('phone', row.get('number', ''))

                    # Send SMS
                    result = self.send_sms(phone, message)

                    if result['status'] == 'sent':
                        results['sent'] += 1
                        if result.get('price'):
                            results['total_cost'] += abs(float(result['price']))
                    else:
                        results['failed'] += 1

                    results['messages'].append(result)

            print(f"\n=== Bulk SMS Summary ===")
            print(f"Sent: {results['sent']}")
            print(f"Failed: {results['failed']}")
            print(f"Total Cost: ${results['total_cost']:.4f}")

        except Exception as e:
            print(f"❌ Bulk SMS failed: {e}")

        return results

    def check_balance(self) -> dict:
        """Check Twilio account balance."""
        if not self.has_twilio:
            return {"error": "Twilio not configured"}

        try:
            balance = self.client.api.v2010.balance.fetch()

            result = {
                "balance": balance.balance,
                "currency": balance.currency
            }

            print(f"💰 Account Balance: {balance.balance} {balance.currency}")

            return result

        except Exception as e:
            print(f"❌ Failed to check balance: {e}")
            return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="SMS Notification Agent")
    parser.add_argument('--to', help='Recipient phone number (E.164 format: +1234567890)')
    parser.add_argument('--message', help='SMS message text')
    parser.add_argument('--bulk', help='CSV file for bulk SMS (needs "phone" column)')
    parser.add_argument('--balance', action='store_true', help='Check Twilio account balance')

    args = parser.parse_args()

    agent = SMSAgent()

    if args.balance:
        # Check balance
        agent.check_balance()

    elif args.bulk:
        # Bulk SMS mode
        print(f"Sending bulk SMS from: {args.bulk}")
        message_template = args.message or "Hello {{name}}, this is an automated message."

        results = agent.send_bulk_sms(args.bulk, message_template)
        print(json.dumps(results, indent=2))

    elif args.to and args.message:
        # Single SMS mode
        result = agent.send_sms(args.to, args.message)
        print(json.dumps(result, indent=2))

    else:
        print("Usage:")
        print("  Single SMS: --to +1234567890 --message 'Your message'")
        print("  Bulk SMS:   --bulk contacts.csv --message 'Hi {{name}}'")
        print("  Balance:    --balance")
        print("\nNote: Phone numbers must be in E.164 format (e.g., +1234567890)")

if __name__ == "__main__":
    main()
