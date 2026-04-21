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

## Quick Deploy

```bash
$ openclaw deploy --agent finance-bot
✓ Agent "finance-bot" is live and running
Connected: QuickBooks, Plaid, Stripe, Bank APIs
```

OpenClaw skips all the complexity.

- You don't need to manage servers.
- You don't need to configure banking integrations manually.
- You don't need to debug agent behavior.
- It just works. 24/7.

## Usage

```bash
# Install the skill
$ openclaw skills install finance-agents
✓ Installed finance-agents v1.0.0

# Generate and send invoice
$ openclaw run invoice-agent create --client "Acme Corp" --hours 40 --rate 150
✓ Invoice created: INV-2024-001
✓ Amount: $6,000.00
✓ PDF generated
✓ Sent to: billing@acme.com
✓ Payment reminders scheduled

# Process expense receipts
$ openclaw run expense-agent scan --folder ./receipts
✓ 12 receipts processed
✓ Categories assigned (AI)
✓ Total expenses: $1,847.32
✓ Synced to QuickBooks
✓ Policy violations: 0

# Reconcile bank accounts
$ openclaw run reconcile-agent run
✓ Connected to 3 bank accounts
✓ 156 transactions matched
✓ 4 discrepancies found
✓ Journal entries created
✓ Report generated
```

## Available Agents

| Agent | What it does |
|-------|--------------|
| `invoice-agent` | Automated invoicing, payment tracking, reminders |
| `expense-agent` | OCR receipt scanning, categorization, compliance |
| `report-agent` | P&L, balance sheets, cash flow, custom reports |
| `reconcile-agent` | Bank reconciliation, transaction matching |
| `tax-agent` | 1099/W-2 generation, deduction tracking, filing |

## Integrations

- **Accounting**: QuickBooks, Xero, FreshBooks, Wave
- **Banking**: Plaid, Yodlee (transaction feeds)
- **Payment**: Stripe, PayPal, Square
- **Payroll**: Gusto, ADP, Paychex

## Environment Variables

```bash
export OPENAI_API_KEY="sk-..."           # Required
export QUICKBOOKS_CLIENT_ID="..."        # QuickBooks
export PLAID_CLIENT_ID="..."             # Banking
export PLAID_SECRET="..."
```
