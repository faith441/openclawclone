---
name: hospitality-agents
description: AI-powered automation for hotels, resorts, and vacation rentals. Agents for reservation management, guest services, housekeeping, revenue management, and guest experience.
homepage: https://github.com/openclaw/industries/hospitality
metadata:
  {
    "openclaw":
      {
        "emoji": "🏨",
        "requires": { "bins": ["python3"], "env": ["OPENAI_API_KEY"] },
        "install":
          [
            {
              "id": "uv",
              "kind": "uv",
              "package": "openai requests twilio",
              "label": "Install Hospitality dependencies (uv)",
            },
          ],
      },
  }
---

# Hospitality & Hotels AI Agents

AI-powered automation for hotels, resorts, vacation rentals, and hospitality businesses.

## Available Agents

### 1. Reservation Management Agent
Multi-channel booking integration (OTAs, GDS), rate optimization, availability management, and automated confirmations.

### 2. Guest Services Agent
24/7 AI chatbot for guest inquiries, local recommendations, room service ordering, and special arrangements.

### 3. Housekeeping Coordinator
Room status tracking, staff scheduling, priority assignments, and inventory management.

### 4. Revenue Management Agent
Demand forecasting, competitor rate monitoring, dynamic pricing, and RevPAR optimization.

### 5. Guest Experience Agent
Guest profile management, preference tracking, loyalty programs, and review monitoring.

## Quick Start

```bash
cd industries/hospitality
pip install -r requirements.txt

export OPENAI_API_KEY="sk-..."
export CLOUDBEDS_API_KEY="..."    # PMS integration
export TWILIO_ACCOUNT_SID="..."   # SMS notifications

cd agents/reservation-agent
python scripts/reservation_agent.py start
```

## Sample Workflow

```python
from hospitality.agents import ReservationAgent

agent = ReservationAgent()
result = agent.process_booking({
    "guest_name": "John Smith",
    "check_in": "2024-04-15",
    "check_out": "2024-04-18",
    "room_type": "Deluxe King",
    "special_requests": "High floor, late check-in"
})

# Checks availability, assigns room, processes payment,
# sends confirmation, schedules pre-arrival email
```

## Integrations

- **PMS**: Cloudbeds, Opera, Mews, eZee
- **Channel Managers**: SiteMinder, RoomRaccoon
- **OTAs**: Booking.com, Expedia, Airbnb
- **Communication**: Twilio, Intercom, SendGrid
- **Payment**: Stripe, Adyen, Shift4

## Multi-Language Support

English, Spanish, French, German, Italian, Portuguese, Chinese, Japanese, Korean, Arabic, Russian
