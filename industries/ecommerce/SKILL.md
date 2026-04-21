---
name: ecommerce-agents
description: AI-powered automation for online stores and retail operations. Agents for inventory management, order processing, customer support, shipping, and product catalog management.
homepage: https://github.com/openclaw/industries/ecommerce
metadata:
  {
    "openclaw":
      {
        "emoji": "🛒",
        "requires": { "bins": ["python3"], "env": ["OPENAI_API_KEY"] },
        "install":
          [
            {
              "id": "uv",
              "kind": "uv",
              "package": "openai requests stripe shopify-api",
              "label": "Install E-commerce dependencies (uv)",
            },
          ],
      },
  }
---

# E-commerce & Retail AI Agents

AI-powered automation for online stores, marketplaces, and retail operations.

## Quick Deploy

```bash
$ openclaw deploy --agent ecommerce-bot
✓ Agent "ecommerce-bot" is live and running
Connected: Shopify, Stripe, ShipStation, Zendesk
```

OpenClaw skips all the complexity.

- You don't need to manage servers.
- You don't need to configure payment gateways manually.
- You don't need to debug agent behavior.
- It just works. 24/7.

## Usage

```bash
# Install the skill
$ openclaw skills install ecommerce-agents
✓ Installed ecommerce-agents v1.0.0

# Process new orders automatically
$ openclaw run order-agent process
✓ 15 new orders found
✓ Inventory validated for all items
✓ Payments captured: $2,847.50
✓ Shipping labels generated
✓ Customers notified

# Handle customer support ticket
$ openclaw run support-agent --ticket "Where is my order #12345?"
✓ Order found: #12345
✓ Status: In transit (UPS)
✓ ETA: Tomorrow by 5 PM
✓ Response sent to customer
✓ Ticket resolved automatically

# Update inventory across channels
$ openclaw run inventory-agent sync
✓ Synced: Shopify ↔ Amazon ↔ eBay
✓ Low stock alerts: 3 products
✓ Reorder suggestions generated
✓ Purchase orders created
```

## Available Agents

| Agent | What it does |
|-------|--------------|
| `order-agent` | End-to-end order fulfillment, payments, notifications |
| `inventory-agent` | Stock tracking, reordering, multi-warehouse management |
| `support-agent` | AI customer service, ticket processing, auto-responses |
| `shipping-agent` | Rate shopping, labels, tracking, delivery exceptions |
| `catalog-agent` | Product enrichment, SEO descriptions, multi-channel sync |

## Integrations

- **Platforms**: Shopify, WooCommerce, BigCommerce, Magento
- **Marketplaces**: Amazon, eBay, Etsy, Walmart
- **Shipping**: ShipStation, Shippo, EasyPost
- **Payment**: Stripe, PayPal, Square
- **Support**: Zendesk, Gorgias, Freshdesk

## Environment Variables

```bash
export OPENAI_API_KEY="sk-..."           # Required
export SHOPIFY_API_KEY="..."             # Shopify store
export STRIPE_API_KEY="..."              # Payments
export SHIPSTATION_KEY="..."             # Shipping
```
