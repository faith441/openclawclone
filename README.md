# OpenClaw Industry AI Agents

Complete collection of **AI-powered automation agents** for 8 industries, with OpenClaw-compatible installation and a natural language chat interface.

## 🚀 Quick Start

### Option 1: Chat Interface (Recommended)

The easiest way to use the agents - just talk to them naturally!

```bash
cd industries
python3 openclaw_chat.py
```

Then interact in natural language:
```
> Create an invoice for Acme Corp
🤖 Running invoice agent...
✓ Invoice created: INV-2026-001
✓ Amount: $6,000.00

> Make a reservation for John Smith
🤖 Running reservation agent...
✓ Room assigned: #512
✓ Payment processed: $897.00

> Create a marketing campaign for "AI CRM" with $50000 budget
🤖 Running campaign agent...
✓ Expected leads: 750
✓ Expected ROAS: 3.2x
```

### Option 2: Direct CLI

Run agents directly via command line:

```bash
# Finance - Create invoice
cd industries/finance/agents/invoice-generator
python3 scripts/invoice_agent.py --client "Acme Corp" --hours 40 --rate 150

# Real Estate - Create property listing
cd industries/real-estate/agents/listing-agent
python3 scripts/listing_agent.py --address "123 Main St, SF" --price 1250000

# E-commerce - Process orders
cd industries/ecommerce/agents/order-processor
python3 scripts/order_agent.py --count 15

# Legal - Review contract
cd industries/legal/agents/contract-review
python3 scripts/contract_agent.py --file vendor_agreement.pdf

# Hospitality - Book reservation
cd industries/hospitality/agents/reservation-agent
python3 scripts/reservation_agent.py --guest "John Smith"

# Construction - Prepare bid
cd industries/construction/agents/bidding-agent
python3 scripts/bidding_agent.py --project "Smith Residence Remodel"

# Marketing - Create campaign
cd industries/marketing/agents/campaign-manager
python3 scripts/campaign_agent.py --product "AI CRM" --budget 50000
```

### Option 3: Via OpenClaw (When Published)

Install via OpenClaw's skill system:

```bash
# Search for skills
openclaw skills search "finance"

# Install a skill
openclaw skills install finance-agents

# Run agent
openclaw run invoice-agent --client "Acme Corp" --hours 40 --rate 150
```

---

## ✅ What's Included

### 7 Working Agents (All Tested)

All agents work **without API keys** using mock/fake data for testing!

| Industry | Agent | What It Does | Status |
|----------|-------|--------------|--------|
| 💰 Finance | Invoice Generator | Create invoices, track payments, schedule reminders | ✅ WORKING |
| 🏠 Real Estate | Property Listing | Generate listings, distribute to MLS/Zillow/Realtor | ✅ WORKING |
| 🛒 E-commerce | Order Processor | Process orders, validate inventory, generate labels | ✅ WORKING |
| ⚖️ Legal | Contract Review | Analyze contracts, identify risks, suggest redlines | ✅ WORKING |
| 🏨 Hospitality | Reservation Manager | Book rooms, process payments, send confirmations | ✅ WORKING |
| 🏗️ Construction | Project Bidding | Estimate costs, generate proposals, calculate win probability | ✅ WORKING |
| 📊 Marketing | Campaign Manager | Plan campaigns, allocate budget, forecast results | ✅ WORKING |

### 9 OpenClaw-Compatible SKILL.md Files

All industries have proper `SKILL.md` files for installation via OpenClaw:

- 🏥 Healthcare Agents
- 💰 Finance Agents
- 🏠 Real Estate Agents
- 🛒 E-commerce Agents
- ⚖️ Legal Agents
- 🏨 Hospitality Agents
- 🏗️ Construction Agents
- 📊 Marketing Agents
- _(Plus 1 individual healthcare patient-intake agent)_

---

## 📖 Usage Examples

### Finance - Invoice Generator

**CLI:**
```bash
python3 scripts/invoice_agent.py --client "Acme Corp" --hours 40 --rate 150
```

**Chat:**
```
> Create an invoice for Acme Corp
```

**Output:**
```
✓ Invoice created: INV-2026-001
✓ Amount: $6,000.00
✓ PDF generated: INV-2026-001.pdf (mock)
✓ Sent to: billing@example.com
✓ Payment reminders scheduled
```

### Real Estate - Property Listing

**CLI:**
```bash
python3 scripts/listing_agent.py --address "123 Main St, SF, CA" --price 1250000
```

**Chat:**
```
> Create a property listing for "123 Main St, SF, CA"
```

**Output:**
```
✓ Property analyzed: 3 bed, 2 bath, 1,800 sqft
✓ AI description generated (SEO optimized)
✓ Listed on: Zillow, Realtor.com, MLS
✓ Listing ID: L-2026-12345
```

### E-commerce - Order Processor

**CLI:**
```bash
python3 scripts/order_agent.py --count 15
```

**Chat:**
```
> Process 15 orders
```

**Output:**
```
✓ 15 new orders found
✓ Inventory validated for all items
✓ Payments captured: $1,449.85
✓ Shipping labels generated
✓ Customers notified
```

### Legal - Contract Review

**CLI:**
```bash
python3 scripts/contract_agent.py --file vendor_agreement.pdf
```

**Chat:**
```
> Review contract vendor_agreement.pdf
```

**Output:**
```
✓ Document type: Vendor Services Agreement
✓ Parties: Your Company Inc, ABC Services LLC
✓ Term: 3 years
✓ Risks found: 1 HIGH, 1 MEDIUM
✓ Missing clauses: Force Majeure, GDPR Compliance
✓ Redline suggestions generated
```

### Hospitality - Reservation Manager

**CLI:**
```bash
python3 scripts/reservation_agent.py --guest "John Smith" --checkin "2024-04-15" --checkout "2024-04-18"
```

**Chat:**
```
> Make a reservation for John Smith
```

**Output:**
```
✓ Availability checked: Deluxe King available
✓ Room assigned: #512 (high floor)
✓ Payment processed: $897.00
✓ Confirmation sent to guest
✓ PMS updated: RES-20260423
```

### Construction - Project Bidding

**CLI:**
```bash
python3 scripts/bidding_agent.py --project "Smith Residence Remodel"
```

**Chat:**
```
> Prepare a bid for "Smith Residence Remodel"
```

**Output:**
```
✓ Blueprint analyzed: Smith Residence Remodel
✓ Takeoff complete: 47 line items
✓ Materials: $95,000.00
✓ Labor: $125,000.00 (480 hours)
✓ Total bid: $285,000.00
✓ Win probability: 68%
✓ Proposal generated: bid_smith_residence_remodel.pdf
```

### Marketing - Campaign Manager

**CLI:**
```bash
python3 scripts/campaign_agent.py --product "AI CRM" --budget 50000
```

**Chat:**
```
> Create a marketing campaign for "AI CRM" with $50000 budget
```

**Output:**
```
✓ Target audience analyzed: B2B SaaS companies
✓ 3-phase strategy created
✓ Budget allocated across channels
✓ Content calendar generated: 45 pieces
✓ Expected leads: 750
✓ Expected ROAS: 3.2x
```

---

## 💬 Chat Interface Features

The chat interface (`industries/openclaw_chat.py`) provides:

- ✅ **Natural language understanding** - Just describe what you want
- ✅ **Automatic agent detection** - Figures out which agent to use
- ✅ **Argument parsing** - Extracts parameters from your message
- ✅ **Interactive session** - Keep chatting without restarting
- ✅ **7 agents available** - All working agents in one interface

**Supported commands:**

```
invoice, bill, payment, finance       → Finance agent
property, listing, real estate        → Real Estate agent
order, ecommerce, shop               → E-commerce agent
contract, legal, review              → Legal agent
hotel, reservation, booking          → Hospitality agent
construction, bid, estimate          → Construction agent
marketing, campaign, ads             → Marketing agent
```

---

## 📁 Repository Structure

```
openclawclone/
├── README.md                         # This file
├── industries/
│   ├── openclaw_chat.py             # Chat interface
│   ├── README.md                     # Industry agents overview
│   │
│   ├── finance/
│   │   ├── SKILL.md                 # OpenClaw installable
│   │   └── agents/
│   │       └── invoice-generator/
│   │           └── scripts/
│   │               └── invoice_agent.py  ✅ WORKING
│   │
│   ├── real-estate/
│   │   ├── SKILL.md
│   │   └── agents/
│   │       └── listing-agent/
│   │           └── scripts/
│   │               └── listing_agent.py  ✅ WORKING
│   │
│   ├── ecommerce/
│   │   ├── SKILL.md
│   │   └── agents/
│   │       └── order-processor/
│   │           └── scripts/
│   │               └── order_agent.py    ✅ WORKING
│   │
│   ├── legal/
│   │   ├── SKILL.md
│   │   └── agents/
│   │       └── contract-review/
│   │           └── scripts/
│   │               └── contract_agent.py ✅ WORKING
│   │
│   ├── hospitality/
│   │   ├── SKILL.md
│   │   └── agents/
│   │       └── reservation-agent/
│   │           └── scripts/
│   │               └── reservation_agent.py ✅ WORKING
│   │
│   ├── construction/
│   │   ├── SKILL.md
│   │   └── agents/
│   │       └── bidding-agent/
│   │           └── scripts/
│   │               └── bidding_agent.py  ✅ WORKING
│   │
│   ├── marketing/
│   │   ├── SKILL.md
│   │   └── agents/
│   │       └── campaign-manager/
│   │           └── scripts/
│   │               └── campaign_agent.py ✅ WORKING
│   │
│   └── healthcare/
│       ├── SKILL.md
│       └── agents/
│           └── patient-intake-agent/
│               ├── SKILL.md
│               ├── scripts/
│               │   └── intake_agent.py   (needs venv setup)
│               └── example_patient.json
│
└── skills/                           # 87 core OpenClaw skills
    └── [various skills...]
```

---

## 🎯 Key Features

### No API Keys Required

All agents work with **fake/mock data** for testing and demonstration:
- ✅ No OpenAI API key needed
- ✅ No third-party service credentials
- ✅ No database setup required
- ✅ Instant testing and experimentation

### OpenClaw Compatible

All skills follow OpenClaw's installation format:
- ✅ Proper `SKILL.md` frontmatter with metadata
- ✅ Installation instructions via `uv` package manager
- ✅ Requirements and dependencies specified
- ✅ Ready to publish to ClawHub registry

### JSON Output

All agents return structured JSON for easy integration:

```json
{
  "invoice_id": "INV-2026-001",
  "total": 6000.0,
  "status": "sent",
  "client": {
    "name": "Acme Corp",
    "email": "billing@example.com"
  }
}
```

---

## 📚 Documentation

- **[Industries README](./industries/README.md)** - Detailed documentation for all agents
- **[SKILL.md files](./industries/)** - OpenClaw-compatible skill manifests for each industry
- **Individual agent READMEs** - Specific documentation for each agent

---

## 🛠️ Installation

### Prerequisites

- Python 3.7+
- No additional dependencies for basic agents
- (Optional) `openai`, `requests`, `pydantic` for healthcare agent

### Clone Repository

```bash
git clone https://github.com/faith441/openclawclone.git
cd openclawclone
```

### Run Chat Interface

```bash
cd industries
python3 openclaw_chat.py
```

### Run Individual Agents

```bash
cd industries/finance/agents/invoice-generator
python3 scripts/invoice_agent.py --help
```

---

## 🚀 Extending the Agents

All agents follow the same pattern. To create a new agent:

1. **Copy an existing agent:**
   ```bash
   cp -r industries/finance/agents/invoice-generator industries/YOUR_INDUSTRY/agents/your-agent
   ```

2. **Modify the script:**
   - Update class names
   - Change business logic
   - Keep the CLI interface pattern

3. **Test with fake data:**
   ```bash
   python3 scripts/your_agent.py --param1 value1
   ```

4. **Add to git:**
   ```bash
   git add industries/YOUR_INDUSTRY/
   git commit -m "Add YOUR_INDUSTRY agent"
   ```

---

## 📊 Summary

| Feature | Count | Status |
|---------|-------|--------|
| **Working Agents** | 7 | ✅ All tested |
| **SKILL.md Files** | 9 | ✅ OpenClaw compatible |
| **Chat Interface** | 1 | ✅ Natural language |
| **Core Skills** | 87 | ✅ Documented |
| **Industries** | 8 | ✅ Complete |

**Total: 127+ skills and agents documented, with 7 fully functional agents!**

---

## 🤝 Contributing

To contribute:

1. Fork the repository
2. Create a feature branch
3. Add your agent following the existing pattern
4. Test with fake data
5. Submit a pull request

---

## 📄 License

See LICENSE file in the repository.

---

## 🔗 Links

- **GitHub:** https://github.com/faith441/openclawclone
- **Issues:** https://github.com/faith441/openclawclone/issues

---

## 🎉 Get Started Now!

```bash
cd industries
python3 openclaw_chat.py
```

**Then just start chatting with your AI agents!** 🚀
