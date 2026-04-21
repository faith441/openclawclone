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

AI-powered automation for real estate agents, brokers, and property management companies.

## Available Agents

### 1. Property Listing Agent
Automatically create, format, and distribute property listings with AI-generated descriptions and photo enhancement.

### 2. Lead Management Agent
Capture, qualify, and nurture leads automatically with scoring, drip campaigns, and CRM integration.

### 3. Showing Scheduler
Smart appointment scheduling with availability matching, route optimization, and feedback collection.

### 4. Contract Processor
Automate document generation, offer/counteroffer tracking, and e-signature workflows.

### 5. Market Analysis Agent
Comparative market analysis, price recommendations, and market trends.

## Quick Start

```bash
cd industries/real-estate
pip install -r requirements.txt

export OPENAI_API_KEY="sk-..."
export ZILLOW_API_KEY="..."
export DOCUSIGN_KEY="..."

cd agents/property-listing-agent
python scripts/listing_agent.py create --property property_data.json
```

## Sample Workflow

```python
from real_estate.agents import PropertyListingAgent

agent = PropertyListingAgent()
listing = agent.create_listing({
    "address": "123 Main St, San Francisco, CA 94102",
    "price": 1250000,
    "bedrooms": 3,
    "bathrooms": 2,
    "sqft": 1800,
    "features": ["hardwood floors", "updated kitchen"],
    "photos": ["img1.jpg", "img2.jpg"]
})

# AI generates optimized description
agent.distribute(listing, platforms=["zillow", "realtor", "mls"])
```

## Integrations

- **MLS Systems**: API integration for listing distribution
- **Platforms**: Zillow, Realtor.com, Redfin
- **E-Signatures**: DocuSign, HelloSign
- **CRM**: Salesforce, HubSpot, Follow Up Boss
