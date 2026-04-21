---
name: construction-agents
description: AI-powered automation for construction companies and contractors. Agents for project bidding, scheduling, materials ordering, site safety, change orders, and daily reporting.
homepage: https://github.com/openclaw/industries/construction
metadata:
  {
    "openclaw":
      {
        "emoji": "🏗️",
        "requires": { "bins": ["python3"], "env": ["OPENAI_API_KEY"] },
        "install":
          [
            {
              "id": "uv",
              "kind": "uv",
              "package": "openai requests pypdf2 pillow",
              "label": "Install Construction dependencies (uv)",
            },
          ],
      },
  }
---

# Construction & Contractors AI Agents

AI-powered automation for construction companies, general contractors, and specialty trades.

## Quick Deploy

```bash
$ openclaw deploy --agent construction-bot
✓ Agent "construction-bot" is live and running
Connected: Procore, QuickBooks, Weather API, Suppliers
```

OpenClaw skips all the complexity.

- You don't need to manage servers.
- You don't need to configure project management integrations manually.
- You don't need to debug agent behavior.
- It just works. 24/7.

## Usage

```bash
# Install the skill
$ openclaw skills install construction-agents
✓ Installed construction-agents v1.0.0

# Generate a project bid
$ openclaw run bidding-agent estimate --plans blueprints.pdf
✓ Blueprint analyzed: Kitchen Remodel
✓ Takeoff complete: 47 line items
✓ Materials: $95,000
✓ Labor: $125,000 (480 hours)
✓ Total bid: $285,000
✓ Win probability: 68%
✓ Proposal generated: bid_smith_residence.pdf

# Create project schedule
$ openclaw run scheduling-agent create --project "Office Build"
✓ Tasks identified: 24
✓ Dependencies mapped
✓ Weather delays factored: +12 days
✓ Critical path: Foundation → Framing → Drywall
✓ Completion: Sept 5, 2024
✓ Gantt chart generated

# Order materials
$ openclaw run materials-agent order --project "Kitchen Remodel"
✓ Material list generated: 156 items
✓ 4 supplier quotes compared
✓ Best price: Home Depot Pro ($8,450)
✓ PO created: PO-2024-001
✓ Delivery scheduled: May 15
```

## Available Agents

| Agent | What it does |
|-------|--------------|
| `bidding-agent` | Automated takeoff, cost estimation, proposal generation |
| `scheduling-agent` | CPM scheduling, resource allocation, weather delays |
| `materials-agent` | Procurement, supplier quotes, purchase orders |
| `safety-agent` | OSHA compliance, incident reporting, daily checklists |
| `change-agent` | Change order processing, cost impact, approvals |
| `daily-agent` | Photo documentation, labor tracking, progress reports |

## Integrations

- **Project Management**: Procore, Buildertrend, CoConstruct
- **Estimating**: PlanSwift, Bluebeam Revu, STACK
- **Accounting**: QuickBooks, Sage 100, Viewpoint
- **Scheduling**: Microsoft Project, Primavera P6
- **Safety**: iAuditor, HammerTech

## Environment Variables

```bash
export OPENAI_API_KEY="sk-..."           # Required
export PROCORE_API_KEY="..."             # Project management
export WEATHER_API_KEY="..."             # Weather forecasting
export QUICKBOOKS_KEY="..."              # Accounting
```
