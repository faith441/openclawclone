# OpenClaw AI Agents - Setup Guide

Complete guide for setting up real API integrations with all agents.

## Quick Start (No API Keys Required!)

These agents work immediately without any setup:
- **PDF Generator** - Create PDFs from text, CSV, or markdown
- **Email Sender** - Send emails (just needs SMTP credentials)

## Industry Agents with Real Integrations

### 1. Finance Agent (Invoice Generator)

**Real Integrations:**
- ✅ Stripe Payment Links
- ✅ Email Sending
- ⏳ QuickBooks (coming soon)

**Setup:**

```bash
# 1. Get Stripe API Key (https://dashboard.stripe.com/apikeys)
export STRIPE_API_KEY="sk_test_..."

# 2. Configure SMTP for email sending
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASS="your-app-password"

# 3. Install dependencies
cd industries/finance/agents/invoice-generator
pip install -r requirements.txt

# 4. Run the agent
python3 scripts/invoice_agent.py --client "Acme Corp" --hours 40 --rate 150 --email "client@example.com"
```

**What it does:**
- Creates professional invoices
- Generates real Stripe payment links
- Sends invoices via email
- Schedules payment reminders

---

### 2. Real Estate Agent (Listing Agent)

**Real Integrations:**
- ✅ Claude AI (property descriptions)
- ✅ OpenAI (alternative to Claude)

**Setup:**

```bash
# 1. Get Anthropic API Key (https://console.anthropic.com/)
export ANTHROPIC_API_KEY="sk-ant-..."

# Or use OpenAI instead:
export OPENAI_API_KEY="sk-..."

# 2. Install dependencies
cd industries/real-estate/agents/listing-agent
pip install -r requirements.txt

# 3. Run the agent
python3 scripts/listing_agent.py \
  --address "123 Main St, San Francisco, CA" \
  --price 1250000 \
  --beds 3 \
  --baths 2 \
  --sqft 1800
```

**What it does:**
- Generates AI-powered property descriptions
- SEO-optimized listings
- Mock distribution to Zillow/Realtor/MLS (real integration coming soon)

---

### 3. E-commerce Agent (Order Processor)

**Real Integrations:**
- ✅ Shopify (order processing)

**Setup:**

```bash
# 1. Get Shopify credentials
# - Go to: Shopify Admin > Apps > Develop apps
# - Create private app
# - Get: Access Token

export SHOPIFY_SHOP_NAME="your-store"  # Just the name, not full URL
export SHOPIFY_ACCESS_TOKEN="shpat_..."

# 2. Install dependencies
cd industries/ecommerce/agents/order-processor
pip install -r requirements.txt

# 3. Run the agent
python3 scripts/order_agent.py --count 10
```

**What it does:**
- Fetches real Shopify orders
- Processes and fulfills orders
- Generates tracking numbers
- Updates order status

---

## Automation Agents (Easy Setup!)

### 4. Email Automation Agent

**Setup:**

```bash
# For Gmail:
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASS="your-app-password"  # Generate at https://myaccount.google.com/apppasswords

# No dependencies needed - uses Python stdlib!
```

**Usage:**

```bash
cd industries/automation/agents/email-sender/scripts

# Send single email
python3 email_agent.py \
  --to "recipient@example.com" \
  --subject "Hello" \
  --body "This is a test email"

# Send bulk emails from CSV
python3 email_agent.py \
  --bulk contacts.csv \
  --subject "Hi {{name}}" \
  --body "Hello {{name}}, welcome to our service!"
```

**CSV Format for Bulk Emails:**
```csv
email,name
john@example.com,John
jane@example.com,Jane
```

---

### 5. SMS Notification Agent

**Setup:**

```bash
# 1. Get Twilio free trial ($15 credit!)
# Sign up at: https://www.twilio.com/try-twilio

# 2. Get credentials from Twilio Console
export TWILIO_ACCOUNT_SID="AC..."
export TWILIO_AUTH_TOKEN="..."
export TWILIO_PHONE_NUMBER="+1234567890"

# 3. Install Twilio library
cd industries/automation/agents/sms-sender
pip install -r requirements.txt
```

**Usage:**

```bash
cd industries/automation/agents/sms-sender/scripts

# Send single SMS
python3 sms_agent.py \
  --to "+11234567890" \
  --message "Hello from OpenClaw!"

# Send bulk SMS from CSV
python3 sms_agent.py \
  --bulk contacts.csv \
  --message "Hi {{name}}, your order is ready!"

# Check account balance
python3 sms_agent.py --balance
```

**CSV Format for Bulk SMS:**
```csv
phone,name
+11234567890,John
+10987654321,Jane
```

---

### 6. PDF Generator Agent

**Setup:**

```bash
# Install dependencies
cd industries/automation/agents/pdf-generator
pip install -r requirements.txt
```

**Usage:**

```bash
cd industries/automation/agents/pdf-generator/scripts

# Text to PDF
python3 pdf_agent.py \
  --text "This is my PDF content" \
  --output document.pdf \
  --title "My Document"

# CSV to PDF table
python3 pdf_agent.py \
  --csv data.csv \
  --output report.pdf \
  --title "Sales Report"

# Markdown to PDF
python3 pdf_agent.py \
  --markdown readme.md \
  --output readme.pdf

# Merge PDFs
python3 pdf_agent.py \
  --merge file1.pdf file2.pdf file3.pdf \
  --output merged.pdf
```

---

## Interactive Chat Interface

The easiest way to use all agents:

```bash
cd industries
python3 openclaw_interactive.py
```

Features:
- ✅ Step-by-step setup wizards
- ✅ Automatic API key detection
- ✅ Configuration validation
- ✅ Real-time feedback

---

## Environment Variables Reference

### Finance Agent
```bash
STRIPE_API_KEY          # Stripe secret key
SMTP_HOST               # Email server (e.g., smtp.gmail.com)
SMTP_PORT               # Email port (default: 587)
SMTP_USER               # Email username
SMTP_PASS               # Email password
FROM_EMAIL              # From address (optional)
```

### Real Estate Agent
```bash
ANTHROPIC_API_KEY       # Claude API key (preferred)
OPENAI_API_KEY          # OpenAI key (alternative)
```

### E-commerce Agent
```bash
SHOPIFY_SHOP_NAME       # Your shop name (e.g., "mystore")
SHOPIFY_ACCESS_TOKEN    # Shopify access token
```

### Email Agent
```bash
SMTP_HOST               # SMTP server
SMTP_PORT               # SMTP port (default: 587)
SMTP_USER               # SMTP username
SMTP_PASS               # SMTP password
```

### SMS Agent
```bash
TWILIO_ACCOUNT_SID      # Twilio account SID
TWILIO_AUTH_TOKEN       # Twilio auth token
TWILIO_PHONE_NUMBER     # Your Twilio phone number
```

---

## Getting API Keys

### Stripe (Finance Agent)
1. Go to https://dashboard.stripe.com/apikeys
2. Create account or login
3. Copy "Secret key" (starts with `sk_test_` or `sk_live_`)
4. Set: `export STRIPE_API_KEY="sk_test_..."`

### Anthropic/Claude (Real Estate Agent)
1. Go to https://console.anthropic.com/
2. Create account
3. Go to API Keys section
4. Create new key
5. Set: `export ANTHROPIC_API_KEY="sk-ant-..."`

### Shopify (E-commerce Agent)
1. Login to Shopify Admin
2. Go to: Apps > Develop apps
3. Create private app
4. Get "Admin API access token"
5. Set:
   ```bash
   export SHOPIFY_SHOP_NAME="your-store"
   export SHOPIFY_ACCESS_TOKEN="shpat_..."
   ```

### Twilio (SMS Agent)
1. Go to https://www.twilio.com/try-twilio
2. Sign up for free trial ($15 credit)
3. Get credentials from console:
   - Account SID
   - Auth Token
   - Phone Number
4. Set:
   ```bash
   export TWILIO_ACCOUNT_SID="AC..."
   export TWILIO_AUTH_TOKEN="..."
   export TWILIO_PHONE_NUMBER="+1234567890"
   ```

### Gmail SMTP (Email Agent)
1. Enable 2-factor authentication on Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate app password for "Mail"
4. Set:
   ```bash
   export SMTP_HOST="smtp.gmail.com"
   export SMTP_PORT="587"
   export SMTP_USER="your-email@gmail.com"
   export SMTP_PASS="app-password-here"
   ```

---

## Troubleshooting

### "API key not configured"
- Make sure you've set the environment variable: `export API_KEY="..."`
- Check spelling of variable name
- Verify key starts with correct prefix (sk_test_, sk-ant-, etc.)

### "Library not installed"
- Run `pip install -r requirements.txt` in the agent directory
- Make sure you're in the correct virtual environment

### "Connection failed"
- Check your internet connection
- Verify API key is valid (not expired/revoked)
- Check API service status

### Email sending fails
- Use app-specific password for Gmail (not your regular password)
- Enable "Less secure app access" if using other providers
- Check SMTP host and port are correct

---

## Cost Estimates

### Stripe
- Payment links: **Free**
- Transaction fees: 2.9% + $0.30 per successful payment

### Claude AI
- ~$3 per 1M input tokens
- ~$15 per 1M output tokens
- Property descriptions: ~$0.01-0.05 each

### Twilio
- Free trial: **$15 credit**
- SMS: $0.0079 per message (US)
- Phone number: $1.15/month

### Email (SMTP)
- Gmail: **Free** (up to 500 emails/day)
- SendGrid: Free tier (100 emails/day)

### PDF Generator
- **Free** (no API needed)

---

## Next Steps

1. **Start with easy agents**: Try Email or PDF generator first
2. **Add API keys gradually**: Set up one integration at a time
3. **Use interactive chat**: Easiest way to test everything
4. **Check costs**: Most services have free tiers perfect for testing

Questions? Check the main README or open an issue on GitHub!
