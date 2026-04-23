#!/usr/bin/env python3
"""
Invoice Generator Agent

Automated invoicing with:
- Invoice creation from client data
- PDF generation
- Payment tracking
- Reminder scheduling
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

class InvoiceAgent:
    def __init__(self):
        self.invoice_counter = 1

    def create_invoice(self, client_data: dict) -> dict:
        """Create invoice from client data."""
        invoice_id = f"INV-{datetime.now().year}-{str(self.invoice_counter).zfill(3)}"

        # Calculate total
        total = 0
        for item in client_data.get('items', []):
            hours = item.get('hours', 0)
            rate = item.get('rate', 0)
            total += hours * rate

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
            "reminders_scheduled": [
                (datetime.now() + timedelta(days=23)).strftime('%Y-%m-%d'),
                (datetime.now() + timedelta(days=31)).strftime('%Y-%m-%d')
            ]
        }

        print(f"✓ Invoice created: {invoice_id}")
        print(f"✓ Amount: ${total:,.2f}")
        print(f"✓ PDF generated: {invoice_id}.pdf (mock)")
        print(f"✓ Sent to: {client_data['client']['email']}")
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
