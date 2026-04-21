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

## Available Agents

### 1. Project Bidding Agent
Automated takeoff from blueprints, cost estimation, labor calculation, and proposal generation with win probability analysis.

### 2. Project Scheduling Agent
CPM scheduling, resource allocation, weather delay predictions, and Gantt chart generation.

### 3. Materials Ordering Agent
Material requirement calculation, supplier quote comparison, purchase order automation, and JIT ordering.

### 4. Site Safety Agent
Daily safety checklists, incident reporting, OSHA compliance monitoring, and near-miss analysis.

### 5. Change Order Manager
Change request intake, cost impact analysis, approval workflows, and timeline assessment.

### 6. Daily Reporting Agent
Photo documentation with AI analysis, weather logging, labor tracking, and progress billing support.

## Quick Start

```bash
cd industries/construction
pip install -r requirements.txt

export OPENAI_API_KEY="sk-..."
export PROCORE_API_KEY="..."       # Project management
export WEATHER_API_KEY="..."       # Weather data

cd agents/bidding-agent
python scripts/bidding_agent.py estimate --plans blueprints.pdf
```

## Sample Workflow

```python
from construction.agents import BiddingAgent

agent = BiddingAgent()
bid = agent.prepare_bid({
    "project_name": "Smith Residence Remodel",
    "location": "San Francisco, CA",
    "plans": "blueprints.pdf",
    "project_type": "residential_remodel"
})

# Returns: total_cost, breakdown (materials, labor, equipment),
# schedule, line_items, win_probability, and proposal PDF
```

## Integrations

- **Project Management**: Procore, Buildertrend, CoConstruct
- **Estimating**: PlanSwift, Bluebeam Revu, STACK
- **Accounting**: QuickBooks, Sage 100, Viewpoint
- **Scheduling**: Microsoft Project, Primavera P6
- **Safety**: iAuditor, HammerTech

## Construction Types

- Residential (single-family, multi-family, remodels)
- Commercial (office, retail, warehouses)
- Specialty (electrical, plumbing, HVAC, roofing)
