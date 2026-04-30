# 🚀 Lovable Quickstart - Deploy in 5 Minutes

## What You're Deploying

A complete **SaaS platform** in 2 parts:
1. **Frontend** (Lovable) - React UI for workflow design
2. **Backend** (Railway) - Flask API + PostgreSQL

## Step 1: Deploy Backend (2 min)

### Option A: One-Click Railway Deploy

Click this button:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/YOUR_USERNAME/zenthral)

### Option B: Manual Railway Deploy

```bash
cd web/
railway login
railway init
railway up
railway add -d postgresql
```

**✅ Copy your backend URL:**
```
https://zenthral-production.up.railway.app
```

## Step 2: Deploy Frontend to Lovable (1 min)

### Upload to Lovable:

1. Go to **https://lovable.dev**
2. Click **"New Project"**
3. Select **"Upload Folder"**
4. Upload: `/lovable-frontend/`
5. Lovable auto-detects it's React/Vite
6. Click **"Deploy"**

### Set Environment Variable:

In Lovable Project Settings:
```
VITE_API_URL = https://zenthral-production.up.railway.app
```
(Use YOUR Railway URL from Step 1)

## Step 3: Test (30 seconds)

1. Open your Lovable URL
2. Register an account
3. Go to Settings → Add API key
4. Go to Create Automation → Test!

## ✅ Done!

Your SaaS is live:
- **Frontend**: `https://your-project.lovable.app`
- **Backend**: `https://zenthral-production.up.railway.app`

## Next Steps

### For Development:
```bash
# Frontend (port 3000)
cd lovable-frontend/
npm install
npm run dev

# Backend (port 5001)
cd web/
source venv/bin/activate
python app.py
```

### For Users (CLI):
```bash
# Test locally first
cd zenthral-cli/
pip install -e .
zenthral --help

# When ready, publish to PyPI
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Costs

- **Lovable**: Free (or $20/month for custom domain)
- **Railway**: $5-20/month
- **Total**: $5-40/month

## Customization

Ask Lovable to customize your app:
- "Add a dark mode toggle"
- "Change colors to purple"
- "Create a pricing page"
- "Add team management"

Lovable will modify and redeploy automatically!

## Need Help?

See complete guide: `DEPLOY_TO_LOVABLE.md`

**You're live in 5 minutes!** 🎉
