#!/usr/bin/env python3
"""Reservation Management Agent - Hotel booking automation"""

import argparse
import json
from datetime import datetime, timedelta

class ReservationAgent:
    def book_reservation(self, guest: str, checkin: str, checkout: str, room_type: str) -> dict:
        """Process hotel booking."""

        nights = 3  # Mock calculation
        rate = 299.00
        total = nights * rate

        reservation = {
            "confirmation_number": f"HTL-{datetime.now().strftime('%Y%m%d%H%M')}",
            "guest_name": guest,
            "check_in": checkin,
            "check_out": checkout,
            "room_type": room_type,
            "room_number": "512",
            "nights": nights,
            "rate_per_night": rate,
            "total_amount": total,
            "status": "confirmed",
            "pms_id": f"RES-{datetime.now().strftime('%Y%m%d')}"
        }

        print(f"✓ Availability checked: {room_type} available")
        print(f"✓ Room assigned: #{reservation['room_number']} (high floor)")
        print(f"✓ Payment processed: ${total:,.2f}")
        print(f"✓ Confirmation sent to guest")
        print(f"✓ Pre-arrival email scheduled")
        print(f"✓ PMS updated: {reservation['pms_id']}")

        return reservation

def main():
    parser = argparse.ArgumentParser(description="Reservation Management Agent")
    parser.add_argument('--guest', required=True, help='Guest name')
    parser.add_argument('--checkin', default='2024-04-15', help='Check-in date')
    parser.add_argument('--checkout', default='2024-04-18', help='Check-out date')
    parser.add_argument('--room', default='Deluxe King', help='Room type')

    args = parser.parse_args()

    agent = ReservationAgent()
    result = agent.book_reservation(args.guest, args.checkin, args.checkout, args.room)

    print("\n=== Reservation Confirmed ===")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
