---
name: finance-agents
description: AI-powered automation for bookkeeping, accounting, and financial management. Agents for invoicing, expense tracking, financial reporting, bank reconciliation, and tax preparation.
homepage: https://github.com/openclaw/industries/finance
metadata:
  {
    "openclaw":
      {
        "emoji": "💰",
        "requires": { "bins": ["python3"], "env": ["OPENAI_API_KEY"] },
        "install":
          [
            {
              "id": "uv",
              "kind": "uv",
              "package": "openai requests plaid-python stripe",
              "label": "Install Finance dependencies (uv)",
            },
          ],
      },
  }
---

# Finance & Accounting AI Agents

AI-powered automation for bookkeeping, accounting, and financial management.

## Available Agents

### 1. Invoice Generator
Automated invoicing with recurring schedules, payment reminders, multi-currency support, and accounting integration.

### 2. Expense Tracker
OCR receipt scanning, AI-powered categorization, mileage tracking, and policy compliance checking.

### 3. Financial Reporter
Automated P&L statements, balance sheets, cash flow reports, and custom report builder.

### 4. Reconciliation Agent
Bank and credit card reconciliation with transaction matching and discrepancy detection.

### 5. Tax Preparation Agent
1099/W-2 generation, deduction tracking, document collection, and filing deadline reminders.

## Quick Start

```bash
cd industries/finance
pip install -r requirements.txt

export OPENAI_API_KEY="sk-..."
export QUICKBOOKS_CLIENT_ID="..."
export PLAID_CLIENT_ID="..."

cd agents/invoice-generator
python scripts/invoice_agent.py create --client client_data.json
```

## Sample Workflow

```python
from finance.agents import InvoiceGenerator

agent = InvoiceGenerator()
invoice = agent.create_invoice({
    "client": {"name": "Acme Corp", "email": "billing@acme.com"},
    "items": [
        {"description": "Consulting Services", "hours": 40, "rate": 150},
        {"description": "Project Management", "hours": 20, "rate": 125}
    ],
    "terms": "NET30"
})

# Generates PDF, sends to client, records in accounting,
# and schedules payment reminders
```

## Integrations

- **Accounting**: QuickBooks, Xero, FreshBooks, Wave
- **Banking**: Plaid, Yodlee (transaction feeds)
- **Payment**: Stripe, PayPal, Square
- **Payroll**: Gusto, ADP, Paychex

## Compliance

- SOC 2 Type II recommended
- PCI DSS for payment data
- Data encryption at rest and in transit
- Role-based access control
