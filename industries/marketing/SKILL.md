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

## Quick Deploy

```bash
$ openclaw deploy --agent marketing-bot
✓ Agent "marketing-bot" is live and running
Connected: Google Ads, Meta Ads, HubSpot, Analytics
```

OpenClaw skips all the complexity.

- You don't need to manage servers.
- You don't need to configure ad platform APIs manually.
- You don't need to debug agent behavior.
- It just works. 24/7.

## Usage

```bash
# Install the skill
$ openclaw skills install marketing-agents
✓ Installed marketing-agents v1.0.0

# Create a marketing campaign
$ openclaw run campaign-agent create --product "AI CRM" --budget 50000
✓ Target audience analyzed: B2B SaaS
✓ 3-phase strategy created
✓ Budget allocated across channels
✓ Content calendar generated: 45 pieces
✓ Expected leads: 750
✓ Expected ROAS: 3.2x

# Generate content
$ openclaw run content-agent write --type blog --topic "AI in Sales 2024"
✓ Keyword research: 12 targets
✓ Outline generated
✓ Blog post written: 1,523 words
✓ SEO score: 85/100
✓ Social posts created: LinkedIn, Twitter, Facebook
✓ Featured image prompt ready

# Analyze campaign performance
$ openclaw run analytics-agent report --period "last 7 days"
✓ Data collected: Google Ads, Meta, Email
✓ Total spend: $8,450
✓ Conversions: 89
✓ ROAS: 14.8x
✓ Insights: 3 recommendations
✓ Report generated: weekly_report.pdf
```

## Available Agents

| Agent | What it does |
|-------|--------------|
| `campaign-agent` | Multi-channel campaigns, budget allocation, A/B testing |
| `content-agent` | Blog posts, ad copy, social content, email newsletters |
| `social-agent` | Content calendar, auto-posting, engagement monitoring |
| `lead-agent` | Lead capture, scoring, qualification, nurturing |
| `analytics-agent` | Data aggregation, automated reports, insights |
| `seo-agent` | Keyword research, on-page optimization, technical audits |
| `email-agent` | Templates, subject lines, segmentation, A/B testing |

## Integrations

- **Advertising**: Google Ads, Meta Ads, LinkedIn, TikTok
- **Automation**: HubSpot, Marketo, ActiveCampaign
- **CRM**: Salesforce, HubSpot CRM, Pipedrive
- **Analytics**: Google Analytics 4, Mixpanel, Segment
- **SEO**: Ahrefs, SEMrush, Moz
- **Social**: Hootsuite, Buffer, Sprout Social

## Environment Variables

```bash
export OPENAI_API_KEY="sk-..."           # Required
export GOOGLE_ADS_API_KEY="..."          # Google Ads
export FACEBOOK_ACCESS_TOKEN="..."       # Meta Ads
export HUBSPOT_API_KEY="..."             # HubSpot
```
