# Zenthral SaaS - Complete Deployment Guide

## What You've Built

A **multi-tenant SaaS platform** where:
- ✅ Users design workflows in your cloud app
- ✅ Workflows execute on **user's infrastructure** (their computer/server)
- ✅ Users bring their own AI API keys (BYOK)
- ✅ You only host the UI + workflow storage (low cost!)

## Architecture Overview

```
┌──────────────────────────────────────────────────┐
│          CLOUD (Your Infrastructure)             │
│                                                  │
│  ┌─────────────┐        ┌──────────────┐       │
│  │   Frontend  │───────▶│   Backend    │       │
│  │  (Lovable)  │        │   (Flask)    │       │
│  │  Vercel     │        │   Railway    │       │
│  └─────────────┘        └──────────────┘       │
│                              │                   │
│                              │ PostgreSQL        │
│                              ▼                   │
│                         ┌─────────┐             │
│                         │Database │             │
│                         └─────────┘             │
└──────────────────────────────────────────────────┘
                              │
                              │ HTTPS API
                              │
┌──────────────────────────────────────────────────┐
│       USER'S INFRASTRUCTURE                      │
│                                                  │
│  ┌─────────────────────────────────────┐        │
│  │   Zenthral CLI (Python Package)     │        │
│  │   - Polls for workflows              │        │
│  │   - Executes locally                 │        │
│  │   - Uses user's API keys             │        │
│  │   - Reports back to cloud            │        │
│  └─────────────────────────────────────┘        │
│                                                  │
│  User's API Keys (stored locally):              │
│  - OPENAI_API_KEY                               │
│  - ANTHROPIC_API_KEY                            │
│  - GOOGLE_API_KEY                               │
└──────────────────────────────────────────────────┘
```

## Project Structure

```
/Users/faithtemporosa/openclawclone/openclawclone/
├── SAAS_ARCHITECTURE.md         # Architecture doc
├── DEPLOYMENT_GUIDE.md          # This file
│
├── web/                         # SaaS Backend (Flask)
│   ├── app.py                   # Main Flask app
│   ├── models/                  # Multi-tenant database models
│   ├── api/v1/                  # REST API endpoints
│   ├── services/                # Business logic
│   └── requirements.txt         # Python dependencies
│
├── lovable-frontend/            # Frontend (React)
│   ├── src/                     # React components
│   ├── package.json             # NPM dependencies
│   └── LOVABLE_IMPORT_GUIDE.md  # How to import to Lovable
│
├── zenthral-cli/                # CLI Package (for users)
│   ├── setup.py                 # PyPI package config
│   ├── zenthral/                # CLI source code
│   │   ├── cli.py               # Entry point
│   │   ├── core/
│   │   │   ├── client.py        # SaaS API client
│   │   │   └── executor.py      # Workflow executor
│   │   └── commands/            # CLI commands
│   └── README.md                # CLI documentation
│
└── scripts/                     # Agent templates (bundled with CLI)
    ├── finance_agent.py
    ├── real_estate_agent.py
    └── web_scraper.py
```

## Deployment Steps

### 1. Deploy Backend (Flask API)

**Option A: Railway (Recommended)**

```bash
cd web/

# Install Railway CLI
npm install -g @railway/cli

# Login & deploy
railway login
railway init
railway up

# Set environment variables
railway variables set SECRET_KEY=your-secret-key
railway variables set DATABASE_URL=postgresql://...

# Get your backend URL
railway status
# Example: https://zenthral-backend-production.up.railway.app
```

**Option B: Render**

1. Go to render.com
2. Create new "Web Service"
3. Connect GitHub repo
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Add environment variables

**Option C: Fly.io**

```bash
cd web/
fly launch
fly deploy
```

### 2. Deploy Frontend (React)

**Option A: Vercel (Recommended)**

```bash
cd lovable-frontend/

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment variable
vercel env add VITE_API_URL production
# Enter: https://zenthral-backend-production.up.railway.app
```

**Option B: Netlify**

1. Connect GitHub repo
2. Build settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
3. Environment variables:
   - `VITE_API_URL` = your backend URL

**Or use Lovable directly:**
1. Import `/lovable-frontend` to Lovable
2. Lovable will auto-deploy
3. Set `VITE_API_URL` in Lovable settings

### 3. Publish CLI to PyPI

```bash
cd zenthral-cli/

# Build package
python setup.py sdist bdist_wheel

# Upload to PyPI
pip install twine
twine upload dist/*

# Now users can install:
# pip install zenthral-cli
```

**For testing before PyPI:**
```bash
cd zenthral-cli/
pip install -e .
zenthral --help
```

### 4. Setup Database

**PostgreSQL (Railway/Render will auto-create)**

If self-hosting:

```bash
# Create database
createdb zenthral

# Run migrations
cd web/
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## User Workflow

### For End Users:

1. **Sign up** at your frontend (e.g., `https://zenthral.vercel.app`)

2. **Install CLI** on their computer:
   ```bash
   pip install zenthral-cli
   ```

3. **Login to CLI**:
   ```bash
   zenthral login
   # Opens browser to authenticate
   ```

4. **Set their AI API keys** (local only):
   ```bash
   export OPENAI_API_KEY=sk-xxxxx
   export ANTHROPIC_API_KEY=sk-ant-xxxxx
   ```

5. **Run workflows**:
   ```bash
   # Run once
   zenthral run

   # Or run as daemon
   zenthral daemon start
   ```

6. **Create workflows** in web UI, they auto-execute locally!

## Monetization Setup

### Stripe Integration

```bash
pip install stripe
```

Add to `web/requirements.txt`:
```
stripe>=5.0.0
```

Create pricing tiers in Stripe:
- Free: $0/month (100 executions)
- Pro: $29/month (unlimited)
- Enterprise: $299/month (teams + SSO)

### Billing API Endpoint

```python
# web/api/v1/billing.py
from flask import Blueprint
import stripe

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@app.route('/api/v1/billing/subscribe', methods=['POST'])
@jwt_required()
def subscribe():
    user_id = get_jwt_identity()
    tier = request.json.get('tier')  # 'pro' or 'enterprise'

    # Create Stripe checkout session
    session = stripe.checkout.Session.create(
        customer_email=current_user.email,
        mode='subscription',
        line_items=[{
            'price': STRIPE_PRICE_IDS[tier],
            'quantity': 1,
        }],
        success_url='https://zenthral.ai/dashboard?success=true',
        cancel_url='https://zenthral.ai/pricing',
    )

    return jsonify({'checkout_url': session.url})
```

## Cost Estimation

### Your Monthly Costs:

**Backend (Railway)**:
- Hobby plan: $5/month
- Pro plan: $20/month (scales with usage)

**Database (PostgreSQL)**:
- Railway includes 512MB free
- Upgrade: $10/month for 2GB

**Frontend (Vercel)**:
- Free tier (perfect for starting)
- Pro: $20/month (custom domains, analytics)

**Total**: **$5-50/month** to run the entire SaaS!

### User's Costs:

Users pay their AI providers directly:
- OpenAI: ~$0.002 per execution (GPT-4)
- Anthropic: ~$0.003 per execution (Claude)
- Google: ~$0.001 per execution (Gemini)

**You don't pay for their AI usage!**

## Security Checklist

- [ ] Enable HTTPS (automatic on Vercel/Railway)
- [ ] Set secure `SECRET_KEY` environment variable
- [ ] Enable CORS only for your frontend domain
- [ ] Rate limit API endpoints
- [ ] Encrypt database at rest
- [ ] Implement GDPR compliance (user data export/delete)
- [ ] Add CSP headers
- [ ] Enable 2FA for admin accounts

## Monitoring

**Backend Monitoring (Railway/Render)**:
- Built-in metrics dashboard
- Add Sentry for error tracking:
  ```bash
  pip install sentry-sdk[flask]
  ```

**Frontend Monitoring (Vercel)**:
- Analytics built-in
- Add PostHog for product analytics

**CLI Usage Tracking**:
- Track via execution reporting API
- Dashboard shows:
  - Total executions
  - Success rate
  - Popular workflows
  - User retention

## Scaling Strategy

### Phase 1: MVP (0-100 users)
- Railway hobby ($5/month)
- Vercel free tier
- Single database instance

### Phase 2: Growth (100-1,000 users)
- Railway pro ($20/month)
- PostgreSQL 2GB ($10/month)
- Add Redis for caching
- CDN for assets

### Phase 3: Scale (1,000+ users)
- Move to AWS/GCP
- Multi-region deployment
- Database replicas
- Load balancer

## Next Steps

1. **Deploy backend** to Railway
2. **Deploy frontend** to Vercel or Lovable
3. **Test the flow**:
   - Sign up → Create workflow → Install CLI → Run locally
4. **Add Stripe** for billing
5. **Marketing**: Productize on Product Hunt, Hacker News
6. **Iterate** based on user feedback!

## Support

**Your SaaS is ready to launch!** 🚀

Key differentiators:
- ✅ Users control their infrastructure (privacy)
- ✅ BYOK model (no markup on AI costs)
- ✅ Works on user's computer (no vendor lock-in)
- ✅ Low hosting costs for you ($5-50/month)
- ✅ Scales infinitely (users scale themselves)

This is the **n8n** / **Temporal** / **Prefect** model - proven and profitable!
