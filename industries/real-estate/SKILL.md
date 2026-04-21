---
name: real-estate-agents
description: AI-powered automation for real estate agents, brokers, and property management. Agents for property listings, lead management, showing scheduling, and contract processing.
homepage: https://github.com/openclaw/industries/real-estate
metadata:
  {
    "openclaw":
      {
        "emoji": "🏠",
        "requires": { "bins": ["python3"], "env": ["OPENAI_API_KEY"] },
        "install":
          [
            {
              "id": "uv",
              "kind": "uv",
              "package": "openai requests pillow",
              "label": "Install Real Estate dependencies (uv)",
            },
          ],
      },
  }
---

# Real Estate AI Agents

AI-powered automation for real estate agents, brokers, and property management.

## Quick Deploy

```bash
$ openclaw deploy --agent real-estate-bot
✓ Agent "real-estate-bot" is live and running
Connected: Zillow, MLS, DocuSign, CRM
```

OpenClaw skips all the complexity.

- You don't need to manage servers.
- You don't need to configure MLS integrations manually.
- You don't need to debug agent behavior.
- It just works. 24/7.

## Usage

```bash
# Install the skill
$ openclaw skills install real-estate-agents
✓ Installed real-estate-agents v1.0.0

# Create a property listing
$ openclaw run listing-agent create --address "123 Main St, SF, CA"
✓ Property analyzed: 3 bed, 2 bath, 1,800 sqft
✓ AI description generated (SEO optimized)
✓ Photos enhanced and staged virtually
✓ Listed on: Zillow, Realtor.com, MLS
✓ Listing ID: L-2024-12345

# Qualify a new lead
$ openclaw run lead-agent qualify --email "buyer@example.com"
✓ Lead captured: Sarah Johnson
✓ Score: 85/100 (Hot Lead)
✓ Budget: $1.2M - $1.5M
✓ Assigned to: agent@realty.com
✓ Drip campaign started

# Schedule a showing
$ openclaw run showing-agent book --property L-2024-12345
✓ Available slots found: 5
✓ Showing booked: Saturday 2:00 PM
✓ Confirmation sent to buyer
✓ Route optimized with 2 other showings
```

## Available Agents

| Agent | What it does |
|-------|--------------|
| `listing-agent` | AI-generated listings, photo enhancement, multi-platform distribution |
| `lead-agent` | Lead capture, scoring, qualification, and nurturing |
| `showing-agent` | Smart scheduling, route optimization, feedback collection |
| `contract-agent` | Document generation, e-signatures, offer tracking |
| `market-agent` | CMA reports, price recommendations, market trends |

## Integrations

- **Platforms**: Zillow, Realtor.com, Redfin, MLS
- **E-Signatures**: DocuSign, HelloSign
- **CRM**: Salesforce, HubSpot, Follow Up Boss

## Environment Variables

```bash
export OPENAI_API_KEY="sk-..."           # Required
export ZILLOW_API_KEY="..."              # Zillow integration
export DOCUSIGN_KEY="..."                # E-signatures
```
