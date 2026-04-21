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

## Available Agents

### 1. Inventory Manager
Automated stock tracking, reordering, and multi-warehouse management with low stock predictions.

### 2. Order Processor
End-to-end order fulfillment with payment processing, shipping labels, and customer notifications.

### 3. Customer Support Agent
AI-powered customer service with natural language ticket processing and automated responses.

### 4. Shipping Coordinator
Rate shopping across carriers, label generation, tracking updates, and delivery exception handling.

### 5. Product Catalog Agent
Product data enrichment with AI, SEO-optimized descriptions, and multi-channel sync.

## Quick Start

```bash
cd industries/ecommerce
pip install -r requirements.txt

export OPENAI_API_KEY="sk-..."
export SHOPIFY_API_KEY="..."
export SHIPSTATION_KEY="..."

cd agents/order-processor
python scripts/order_agent.py process
```

## Sample Workflow

```python
from ecommerce.agents import OrderProcessor

agent = OrderProcessor()
result = agent.process({
    "order_id": "ORD-12345",
    "customer": {"name": "Jane Smith", "email": "jane@example.com"},
    "items": [{"sku": "PROD-001", "quantity": 2, "price": 29.99}],
    "total": 59.98
})

# Automatically validates inventory, charges payment,
# generates shipping label, and sends confirmation
```

## Integrations

- **Platforms**: Shopify, WooCommerce, BigCommerce, Magento
- **Marketplaces**: Amazon, eBay, Etsy, Walmart
- **Shipping**: ShipStation, Shippo, EasyPost
- **Payment**: Stripe, PayPal, Square
- **Support**: Zendesk, Gorgias, Freshdesk
