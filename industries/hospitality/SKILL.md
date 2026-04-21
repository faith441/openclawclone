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

## Quick Deploy

```bash
$ openclaw deploy --agent hospitality-bot
✓ Agent "hospitality-bot" is live and running
Connected: Cloudbeds, Booking.com, Twilio, Stripe
```

OpenClaw skips all the complexity.

- You don't need to manage servers.
- You don't need to configure OTA integrations manually.
- You don't need to debug agent behavior.
- It just works. 24/7.

## Usage

```bash
# Install the skill
$ openclaw skills install hospitality-agents
✓ Installed hospitality-agents v1.0.0

# Process a new booking
$ openclaw run reservation-agent book --guest "John Smith" --dates "Apr 15-18"
✓ Availability checked: Deluxe King available
✓ Room assigned: #512 (high floor per request)
✓ Payment processed: $897.00
✓ Confirmation sent to guest
✓ Pre-arrival email scheduled
✓ PMS updated: RES-789012

# Handle guest inquiry (AI concierge)
$ openclaw run guest-agent respond --message "Good Italian restaurant nearby?"
✓ Guest profile loaded: John Smith, Room 512
✓ Preferences analyzed
✓ 3 restaurants recommended
✓ Response sent via SMS
✓ Reservation offer included

# Optimize room pricing
$ openclaw run revenue-agent optimize --dates "May 1-31"
✓ Demand forecast generated
✓ Competitor rates analyzed
✓ 23 price adjustments recommended
✓ Expected revenue increase: +9.5%
✓ Changes applied to PMS
```

## Available Agents

| Agent | What it does |
|-------|--------------|
| `reservation-agent` | Multi-channel bookings, availability, confirmations |
| `guest-agent` | 24/7 AI concierge, recommendations, service requests |
| `housekeeping-agent` | Room status, staff scheduling, inventory |
| `revenue-agent` | Dynamic pricing, demand forecasting, RevPAR optimization |
| `experience-agent` | Guest profiles, loyalty programs, review monitoring |

## Integrations

- **PMS**: Cloudbeds, Opera, Mews, eZee
- **Channel Managers**: SiteMinder, RoomRaccoon
- **OTAs**: Booking.com, Expedia, Airbnb
- **Communication**: Twilio, Intercom, SendGrid
- **Payment**: Stripe, Adyen, Shift4

## Environment Variables

```bash
export OPENAI_API_KEY="sk-..."           # Required
export CLOUDBEDS_API_KEY="..."           # PMS integration
export TWILIO_ACCOUNT_SID="..."          # SMS notifications
export TWILIO_AUTH_TOKEN="..."
```
