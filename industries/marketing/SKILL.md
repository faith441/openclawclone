---
name: marketing-agents
description: AI-powered automation for marketing teams and agencies. Agents for campaign management, content creation, social media, lead generation, analytics, SEO, and email marketing.
homepage: https://github.com/openclaw/industries/marketing
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["python3"], "env": ["OPENAI_API_KEY"] },
        "install":
          [
            {
              "id": "uv",
              "kind": "uv",
              "package": "openai requests google-api-python-client",
              "label": "Install Marketing dependencies (uv)",
            },
          ],
      },
  }
---

# Marketing & Advertising AI Agents

AI-powered automation for marketing agencies, in-house teams, and digital advertisers.

## Available Agents

### 1. Campaign Manager Agent
Multi-channel campaign planning, budget allocation, A/B test management, and ROI analysis.

### 2. Content Creation Agent
AI-powered blog posts, social media content, ad copy, email newsletters, and landing page copy.

### 3. Social Media Manager Agent
Content calendar, auto-posting, engagement monitoring, hashtag optimization, and social listening.

### 4. Lead Generation Agent
Landing page optimization, lead scoring, automated email sequences, and CRM integration.

### 5. Analytics & Reporting Agent
Multi-channel data aggregation, automated reports, anomaly detection, and predictive analytics.

### 6. SEO Optimization Agent
Keyword research, on-page SEO analysis, content gap identification, and technical SEO audits.

### 7. Email Marketing Agent
Template generation, subject line optimization, list segmentation, and A/B testing automation.

## Quick Start

```bash
cd industries/marketing
pip install -r requirements.txt

export OPENAI_API_KEY="sk-..."
export GOOGLE_ADS_API_KEY="..."
export FACEBOOK_ACCESS_TOKEN="..."
export HUBSPOT_API_KEY="..."

cd agents/campaign-manager-agent
python scripts/campaign_agent.py create --type "product_launch"
```

## Sample Workflow

```python
from marketing.agents import CampaignManager

agent = CampaignManager()
campaign = agent.create_campaign({
    "product": "AI-Powered CRM Software",
    "target_audience": "B2B SaaS companies",
    "budget": 50000,
    "duration": "3 months",
    "channels": ["google_ads", "linkedin_ads", "email"]
})

# Returns: strategy phases, content calendar, KPIs,
# and expected performance metrics
```

## Integrations

- **Advertising**: Google Ads, Meta Ads, LinkedIn, TikTok
- **Automation**: HubSpot, Marketo, ActiveCampaign
- **CRM**: Salesforce, HubSpot CRM, Pipedrive
- **Analytics**: Google Analytics 4, Mixpanel, Segment
- **SEO**: Ahrefs, SEMrush, Moz
- **Social**: Hootsuite, Buffer, Sprout Social

## AI Capabilities

- Natural language content generation
- Image generation (DALL-E, Midjourney)
- Predictive analytics and forecasting
- Dynamic personalization
