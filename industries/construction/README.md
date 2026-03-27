# Construction & Contractors AI Agents

AI-powered automation for construction companies, general contractors, and specialty trades.

## 🏗️ Available Agents

### 1. Project Bidding Agent
Automated bid preparation, cost estimation, and proposal generation.

**Features:**
- Takeoff automation from blueprints
- Material cost estimation
- Labor hour calculation
- Subcontractor bid management
- Proposal document generation
- Win probability analysis

**Use Cases:**
- Residential construction bids
- Commercial project proposals
- Government contract bids (prevailing wage)
- Emergency/repair quotes

### 2. Project Scheduling Agent
Construction project planning and timeline management.

**Features:**
- CPM (Critical Path Method) scheduling
- Resource allocation and leveling
- Weather delay predictions
- Dependency management
- Gantt chart generation
- Schedule updates and forecasting

**Integrations:**
- Procore, Buildertrend, CoConstruct
- Microsoft Project
- Primavera P6

### 3. Materials Ordering Agent
Automated procurement and inventory management.

**Features:**
- Material requirement calculation
- Supplier quote comparison
- Purchase order automation
- Delivery scheduling
- Inventory tracking
- Just-in-time ordering

**Integrations:**
- Supplier portals (HD, Lowe's, lumber yards)
- Accounting systems (QuickBooks)
- ERP systems

### 4. Site Safety Agent
Safety compliance monitoring and incident management.

**Features:**
- Daily safety checklist automation
- Incident reporting and tracking
- OSHA compliance monitoring
- Safety training scheduling
- PPE tracking
- Near-miss analysis

**Compliance:**
- OSHA regulations
- State-specific requirements
- Company safety policies

### 5. Change Order Manager
Automated change order processing and approval workflows.

**Features:**
- Change request intake
- Cost impact analysis
- Approval workflow automation
- Timeline impact assessment
- Document generation
- Client communication

### 6. Daily Reporting Agent
Automated job site reports and documentation.

**Features:**
- Photo documentation with AI analysis
- Weather logging
- Labor and equipment hours
- Work completed tracking
- Issue identification
- Progress billing support

## Quick Start

```bash
# Navigate to construction
cd industries/construction

# Install dependencies
pip install -r requirements.txt

# Configure
export OPENAI_API_KEY="sk-..."
export PROCORE_API_KEY="..."       # Project management
export QUICKBOOKS_KEY="..."        # Accounting
export WEATHER_API_KEY="..."       # Weather data

# Run bidding agent
cd agents/bidding-agent
python scripts/bidding_agent.py estimate --plans blueprints.pdf
```

## Sample Workflows

### Automated Bid Preparation

```python
from construction.agents import BiddingAgent

agent = BiddingAgent()

# New project to bid
project = {
    "project_name": "Smith Residence Remodel",
    "location": "San Francisco, CA",
    "plans": "blueprints.pdf",
    "specifications": "specs.pdf",
    "bid_date": "2024-04-15",
    "project_type": "residential_remodel"
}

# Generate bid automatically
bid = agent.prepare_bid(project)

print(bid)
# {
#   "project": "Smith Residence Remodel",
#   "total_cost": 285000.00,
#   "breakdown": {
#     "materials": 95000.00,
#     "labor": 125000.00,
#     "equipment": 15000.00,
#     "subcontractors": 35000.00,
#     "overhead": 10000.00,
#     "profit": 5000.00
#   },
#   "schedule": "12 weeks",
#   "line_items": [
#     {"item": "Demolition", "cost": 8500, "hours": 40},
#     {"item": "Framing", "cost": 32000, "hours": 200},
#     {"item": "Electrical", "cost": 18500, "subcontractor": "ABC Electric"},
#     ...
#   ],
#   "win_probability": 0.68,
#   "margin": 1.75,
#   "proposal_pdf": "bid_smith_residence.pdf"
# }
```

### Project Schedule Generation

```python
from construction.agents import SchedulingAgent

agent = SchedulingAgent()

# Create project schedule
schedule = agent.create_schedule({
    "project_name": "Office Building Construction",
    "start_date": "2024-05-01",
    "scope": [
        {"task": "Site Preparation", "duration": 10, "crew_size": 4},
        {"task": "Foundation", "duration": 15, "depends_on": ["Site Preparation"]},
        {"task": "Framing", "duration": 30, "depends_on": ["Foundation"]},
        {"task": "Electrical Rough-in", "duration": 12, "depends_on": ["Framing"]},
        {"task": "Plumbing Rough-in", "duration": 12, "depends_on": ["Framing"]},
        {"task": "Drywall", "duration": 20, "depends_on": ["Electrical Rough-in", "Plumbing Rough-in"]},
        {"task": "Finishes", "duration": 25, "depends_on": ["Drywall"]},
        {"task": "Final Inspection", "duration": 3, "depends_on": ["Finishes"]}
    ],
    "weather_location": "Seattle, WA"
})

print(schedule)
# {
#   "total_duration": "127 days (with weather delays)",
#   "completion_date": "2024-09-05",
#   "critical_path": ["Site Prep → Foundation → Framing → Drywall → Finishes"],
#   "float_days": {
#     "Electrical": 0,
#     "Plumbing": 3
#   },
#   "weather_delays": 12,
#   "gantt_chart": "schedule_gantt.pdf",
#   "milestones": [
#     {"milestone": "Foundation Complete", "date": "2024-05-26"},
#     {"milestone": "Dry-in", "date": "2024-07-05"},
#     {"milestone": "Final Completion", "date": "2024-09-05"}
#   ]
# }
```

### Materials Ordering Automation

```python
from construction.agents import MaterialsAgent

agent = MaterialsAgent()

# Calculate materials needed
materials = agent.calculate_materials({
    "project": "Kitchen Remodel",
    "scope": {
        "cabinets": "12 linear feet upper, 15 linear feet lower",
        "countertops": "granite, 45 sq ft",
        "flooring": "hardwood, 280 sq ft",
        "appliances": ["refrigerator", "range", "dishwasher", "microwave"],
        "electrical": "6 outlets, 4 light fixtures",
        "plumbing": "sink, faucet, garbage disposal"
    }
})

# Get quotes from suppliers
quotes = agent.get_supplier_quotes(materials.items)

# Generate purchase orders
pos = agent.create_purchase_orders(quotes, delivery_date="2024-05-15")

print(pos)
# [
#   {
#     "po_number": "PO-2024-001",
#     "supplier": "Home Depot Pro",
#     "total": 8,450.00,
#     "items": ["2x4 studs (100)", "Drywall (40 sheets)", "Screws/nails"],
#     "delivery_date": "2024-05-15",
#     "status": "submitted"
#   },
#   {
#     "po_number": "PO-2024-002",
#     "supplier": "ABC Cabinets",
#     "total": 6,200.00,
#     "items": ["Custom kitchen cabinets"],
#     "lead_time": "6 weeks",
#     "delivery_date": "2024-06-26"
#   }
# ]
```

## Integrations

### Project Management Software
- **Procore**: Construction management platform
- **Buildertrend**: Residential construction software
- **CoConstruct**: Custom builder software
- **PlanGrid**: Field collaboration

### Estimating & Takeoff
- **PlanSwift**: Digital takeoff software
- **Bluebeam Revu**: PDF markup and takeoff
- **On-Screen Takeoff**: Estimating software
- **STACK**: Cloud-based takeoff

### Accounting & Financial
- **QuickBooks**: Small business accounting
- **Sage 100 Contractor**: Construction accounting
- **Foundation**: Construction accounting
- **Viewpoint**: ERP for construction

### Scheduling Tools
- **Microsoft Project**: Project scheduling
- **Primavera P6**: Enterprise scheduling
- **Smartsheet**: Collaborative planning

### Safety & Compliance
- **Safety Reports**: Incident management
- **iAuditor**: Safety inspection app
- **GoCanvas**: Mobile forms
- **HammerTech**: Safety management system

## Construction Types Supported

### Residential
- Single-family homes
- Multi-family developments
- Remodels and additions
- Custom homes

### Commercial
- Office buildings
- Retail spaces
- Warehouses
- Industrial facilities

### Specialty
- Concrete work
- Electrical contracting
- Plumbing
- HVAC
- Roofing
- Landscaping

## Estimating Database

Built-in cost databases with regional pricing:
- **RSMeans**: Industry-standard cost data
- **National Construction Estimator**: Craftsman pricing
- **Local supplier pricing**: Real-time integration
- **Historical project data**: Company-specific costs
- **Labor rates**: Union and non-union by trade

## Safety Compliance

### OSHA Requirements
✅ **Required Documentation:**
- Daily toolbox talks
- Site-specific safety plans
- Hazard communication
- Fall protection plans
- Confined space permits
- Hot work permits

### Incident Tracking
- Near-miss reporting
- Accident investigation
- Corrective actions
- Trend analysis
- Safety metrics

## Metrics & KPIs

### Project Performance
- **Budget variance**: Actual vs. estimated costs
- **Schedule variance**: On-time completion rate
- **Change order rate**: % of projects with changes
- **Rework**: Defect and redo tracking
- **Productivity**: Labor hours per unit

### Financial Metrics
- **Gross profit margin**
- **Overhead recovery rate**
- **Accounts receivable aging**
- **Work-in-progress (WIP)**
- **Cash flow**

### Safety Metrics
- **TRIR** (Total Recordable Incident Rate)
- **DART** (Days Away, Restricted, or Transferred)
- **Near-miss frequency**
- **Safety training completion**
- **Inspection scores**

## Cost Estimates

### Per construction company (10-20 employees)
- **OpenAI GPT-4**: ~$150-300/month (bidding, documentation)
- **Project Management**: ~$500-1,000/month (Procore, Buildertrend)
- **Estimating Software**: ~$200-400/month
- **Safety Management**: ~$100-200/month
- **Infrastructure**: ~$100-150/month
- **Total**: ~$1,050-2,050/month

### ROI Benefits
- **Bid preparation time**: 60% faster (8 hours → 3 hours)
- **Win rate**: +15-20% improvement
- **Change order disputes**: -40% reduction
- **Safety incidents**: -30% reduction
- **Material waste**: -15% reduction

## Agent Structures

### Bidding Agent
```
bidding-agent/
├── scripts/
│   ├── bidding_agent.py        # Main estimator
│   ├── takeoff.py              # Blueprint analysis
│   ├── cost_calculator.py      # Cost estimation
│   └── proposal_generator.py   # Document creation
├── databases/
│   ├── rsmeans.db              # Cost database
│   ├── suppliers.db            # Supplier pricing
│   └── historical.db           # Past projects
├── templates/
│   ├── residential_bid.docx
│   ├── commercial_bid.docx
│   └── government_bid.docx
├── config.yaml
├── requirements.txt
└── README.md
```

### Scheduling Agent
```
scheduling-agent/
├── scripts/
│   ├── scheduling_agent.py     # CPM scheduler
│   ├── resource_leveling.py    # Resource optimization
│   ├── weather_integration.py  # Weather delays
│   └── gantt_generator.py      # Chart creation
├── templates/
│   └── schedule_templates/
├── config.yaml
├── requirements.txt
└── README.md
```

## Weather Integration

Automatic weather delay predictions:
- Historical weather data analysis
- 14-day forecasts
- Weather-sensitive task identification
- Schedule buffer recommendations
- Real-time alerts

## Prevailing Wage Support

For government/public works projects:
- Certified payroll reporting
- Prevailing wage rate tables
- Davis-Bacon compliance
- Fringe benefit tracking
- Audit trail

## Blueprint & Plan Analysis

AI-powered document analysis:
- PDF/CAD file ingestion
- Automated quantity takeoff
- Room/area measurement
- Material list generation
- Spec sheet parsing

## Mobile App Integration

Field worker access via mobile:
- Daily time tracking
- Photo documentation
- Material delivery confirmation
- RFI (Request for Information) submission
- Safety checklist completion
- Progress updates

## Subcontractor Management

- Bid request distribution
- Quote comparison
- Qualification tracking
- Insurance verification
- Lien waiver collection
- Performance ratings

## Testing

```bash
# Bid accuracy tests
pytest tests/bidding/

# Schedule optimization
pytest tests/scheduling/

# Compliance validation
pytest tests/compliance/

# Integration tests
pytest tests/integration/
```

## Deployment

### Cloud Deployment
```yaml
# docker-compose.yml
version: '3.8'

services:
  bidding-agent:
    build: ./agents/bidding-agent
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - RSMEANS_API_KEY=${RSMEANS_API_KEY}
    ports:
      - "8020:8000"
    volumes:
      - ./plans:/app/plans

  scheduling-agent:
    build: ./agents/scheduling-agent
    environment:
      - WEATHER_API_KEY=${WEATHER_API_KEY}
    ports:
      - "8021:8000"

  materials-agent:
    build: ./agents/materials-agent
    environment:
      - QUICKBOOKS_API_KEY=${QUICKBOOKS_API_KEY}
    ports:
      - "8022:8000"
```

## Training & Certification

### Recommended Training
- Construction Management Fundamentals
- Safety compliance (OSHA 10/30)
- Estimating best practices
- Project scheduling
- Contract administration

### Industry Certifications
- CCM (Certified Construction Manager)
- LEED AP (for green building)
- PMP (Project Management Professional)
- CPE (Certified Professional Estimator)

## Documentation

See `/agents/*/README.md` for individual agent documentation and implementation guides.
