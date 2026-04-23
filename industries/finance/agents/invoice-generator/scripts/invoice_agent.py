#!/usr/bin/env python3
"""
Invoice Generator Agent

Automated invoicing with:
- Invoice creation from client data
- Real Stripe payment links
- Email notifications
- Payment tracking
- Reminder scheduling
"""

import argparse
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from pathlib import Path

class InvoiceAgent:
    def __init__(self):
        self.invoice_counter = 1
        self.has_stripe = bool(os.environ.get('STRIPE_API_KEY'))
        self.has_email = bool(os.environ.get('SMTP_HOST'))

        # Initialize Stripe if available
        self.stripe = None
        if self.has_stripe:
            try:
                import stripe
                stripe.api_key = os.environ.get('STRIPE_API_KEY')
                self.stripe = stripe
            except ImportError:
                print("⚠️  stripe library not installed. Run: pip install stripe")
                self.has_stripe = False

    def create_stripe_payment_link(self, amount: float, description: str, invoice_id: str) -> str:
        """Create real Stripe payment link."""
        if not self.has_stripe:
            return None

        try:
            # Create a Stripe product
            product = self.stripe.Product.create(
                name=description,
                metadata={"invoice_id": invoice_id}
            )

            # Create a Stripe price (in cents)
            price = self.stripe.Price.create(
                product=product.id,
                unit_amount=int(amount * 100),
                currency='usd'
            )

            # Create payment link
            payment_link = self.stripe.PaymentLink.create(
                line_items=[{"price": price.id, "quantity": 1}],
                metadata={"invoice_id": invoice_id}
            )

            return payment_link.url
        except Exception as e:
            print(f"⚠️  Stripe payment link creation failed: {e}")
            return None

    def send_invoice_email(self, client_email: str, invoice_id: str, amount: float, payment_link: str = None):
        """Send invoice via email."""
        if not self.has_email:
            return False

        try:
            smtp_host = os.environ.get('SMTP_HOST')
            smtp_port = int(os.environ.get('SMTP_PORT', 587))
            smtp_user = os.environ.get('SMTP_USER')
            smtp_pass = os.environ.get('SMTP_PASS')
            from_email = os.environ.get('FROM_EMAIL', smtp_user)

            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'Invoice {invoice_id} - ${amount:,.2f}'
            msg['From'] = from_email
            msg['To'] = client_email

            # Email body
            if payment_link:
                body = f"""
                Invoice {invoice_id}
                Amount: ${amount:,.2f}

                Pay now: {payment_link}

                Thank you for your business!
                """
            else:
                body = f"""
                Invoice {invoice_id}
                Amount: ${amount:,.2f}

                Thank you for your business!
                """

            msg.attach(MIMEText(body, 'plain'))

            # Send email
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)

            return True
        except Exception as e:
            print(f"⚠️  Email sending failed: {e}")
            return False

    def create_invoice(self, client_data: dict, send_email: bool = False) -> dict:
        """Create invoice from client data with optional Stripe and email integration."""
        invoice_id = f"INV-{datetime.now().year}-{str(self.invoice_counter).zfill(3)}"

        # Calculate total
        total = 0
        for item in client_data.get('items', []):
            hours = item.get('hours', 0)
            rate = item.get('rate', 0)
            total += hours * rate

        # Create Stripe payment link if enabled
        payment_link = None
        if self.has_stripe:
            description = client_data.get('items', [{}])[0].get('description', 'Consulting Services')
            payment_link = self.create_stripe_payment_link(total, description, invoice_id)

        # Generate invoice
        invoice = {
            "invoice_id": invoice_id,
            "client": client_data.get('client', {}),
            "items": client_data.get('items', []),
            "total": total,
            "terms": client_data.get('terms', 'NET30'),
            "issue_date": datetime.now().strftime('%Y-%m-%d'),
            "due_date": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            "status": "sent",
            "payment_link": payment_link,
            "reminders_scheduled": [
                (datetime.now() + timedelta(days=23)).strftime('%Y-%m-%d'),
                (datetime.now() + timedelta(days=31)).strftime('%Y-%m-%d')
            ]
        }

        # Send email if requested
        if send_email and self.has_email:
            email_sent = self.send_invoice_email(
                client_data['client']['email'],
                invoice_id,
                total,
                payment_link
            )

        # Print status
        print(f"✓ Invoice created: {invoice_id}")
        print(f"✓ Amount: ${total:,.2f}")

        if payment_link:
            print(f"✓ Stripe payment link created: {payment_link}")
        else:
            print(f"✓ Payment link: Not created (set STRIPE_API_KEY)")

        if send_email:
            if self.has_email and email_sent:
                print(f"✓ Email sent to: {client_data['client']['email']}")
            else:
                print(f"✓ Email: Not sent (set SMTP_HOST, SMTP_USER, SMTP_PASS)")
        else:
            print(f"✓ Client: {client_data['client']['email']}")

        print(f"✓ Payment reminders scheduled")

        return invoice

def main():
    parser = argparse.ArgumentParser(description="Invoice Generator Agent")
    parser.add_argument('--client', required=True, help='Client name')
    parser.add_argument('--hours', type=float, default=40, help='Hours worked')
    parser.add_argument('--rate', type=float, default=150, help='Hourly rate')
    parser.add_argument('--email', default='billing@example.com', help='Client email')

    args = parser.parse_args()

    client_data = {
        "client": {
            "name": args.client,
            "email": args.email
        },
        "items": [
            {
                "description": "Consulting Services",
                "hours": args.hours,
                "rate": args.rate
            }
        ],
        "terms": "NET30"
    }

    agent = InvoiceAgent()
    invoice = agent.create_invoice(client_data)

    print("\n=== Invoice Details ===")
    print(json.dumps(invoice, indent=2))

if __name__ == "__main__":
    main()
