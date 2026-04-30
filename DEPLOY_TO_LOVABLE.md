# Deploy Zenthral to Lovable - Complete Guide

## 🎯 What Goes Where

### ✅ To Lovable (Frontend)
- React app in `/lovable-frontend/`
- Workflow designer UI
- Dashboard
- Settings page
- Auto-deployed by Lovable

### 🚀 To Railway (Backend)
- Python Flask API in `/web/`
- Database (PostgreSQL)
- Workflow storage
- User management

### 📦 To PyPI (CLI)
- Python package in `/zenthral-cli/`
- Users install: `pip install zenthral-cli`

## 📋 Step-by-Step Deployment

### Step 1: Deploy Backend (Railway) - 2 minutes

**One-Click Deploy:**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

**Or Manual:**

```bash
cd web/

# Install Railway CLI
npm install -g @railway/cli

# Login & deploy
railway login
railway init
railway up

# Add PostgreSQL
railway add -d postgresql

# Set environment variables
railway variables set SECRET_KEY=$(openssl rand -hex 32)
railway variables set JWT_SECRET_KEY=$(openssl rand -hex 32)

# Get your backend URL
railway status
```

**Copy this URL** - you'll need it for Lovable!
Example: `https://zenthral-production.up.railway.app`

---

### Step 2: Deploy Frontend (Lovable) - 1 minute

**Option A: Import Project to Lovable (Recommended)**

1. Go to **https://lovable.dev**
2. Click **"New Project"**
3. Select **"Import from Files"**
4. Upload the entire `/lovable-frontend/` folder
5. Lovable will auto-detect it's a React/Vite project
6. Click **"Deploy"**

**Option B: Import from GitHub**

1. Push `/lovable-frontend/` to GitHub
2. In Lovable, select **"Import from GitHub"**
3. Connect your repo
4. Select `lovable-frontend` directory
5. Deploy!

---

### Step 3: Configure Environment Variables in Lovable

After importing to Lovable:

1. Go to **Project Settings** → **Environment Variables**
2. Add this variable:

```
VITE_API_URL=https://zenthral-production.up.railway.app
```

(Replace with YOUR Railway backend URL from Step 1)

3. **Redeploy** the Lovable project

---

### Step 4: Test Your SaaS

1. Open your Lovable URL (e.g., `https://your-project.lovable.app`)
2. Click **"Register"**
3. Create an account
4. Login
5. Go to **Settings** → Add an API key
6. Go to **Create Automation** → Test workflow generation!

---

## 🎨 Customize in Lovable

Once deployed, you can ask Lovable to customize:

**Ask Lovable:**
- "Change the color scheme to purple"
- "Add a dark mode toggle"
- "Create a new page for team management"
- "Add a pricing page"
- "Customize the dashboard widgets"

Lovable will update the code and redeploy automatically!

---

## 📦 Publish CLI to PyPI (Optional - For User Distribution)

When you're ready for users to install your CLI:

```bash
cd zenthral-cli/

# Build package
python setup.py sdist bdist_wheel

# Upload to PyPI
pip install twine
twine upload dist/*
```

Then users can:
```bash
pip install zenthral-cli
zenthral login
```

For now, you can test locally:
```bash
cd zenthral-cli/
pip install -e .
zenthral --help
```

---

## 🔐 Security Checklist

After deploying:

- [ ] Set strong `SECRET_KEY` and `JWT_SECRET_KEY` in Railway
- [ ] Enable HTTPS (automatic on Railway & Lovable)
- [ ] Set CORS to only allow your Lovable domain
- [ ] Enable Railway's built-in rate limiting
- [ ] Add monitoring (Sentry, LogRocket)

---

## 💰 Costs

### Development (Free Tier)
- **Lovable**: Free preview deployments
- **Railway**: $5/month (includes 512MB DB)
- **Total**: $5/month

### Production
- **Lovable**: $20/month (custom domain + analytics)
- **Railway**: $20/month (Pro plan)
- **PostgreSQL**: Included with Railway
- **Total**: $40/month

---

## 🚀 Complete Architecture

```
┌─────────────────────────────────────┐
│   Lovable (Frontend)                │
│   https://your-app.lovable.app      │
│   - React UI                        │
│   - Workflow designer               │
│   - Dashboard                       │
└────────────┬────────────────────────┘
             │
             │ HTTPS API calls
             ↓
┌─────────────────────────────────────┐
│   Railway (Backend)                 │
│   https://zenthral.up.railway.app   │
│   - Flask API                       │
│   - PostgreSQL                      │
│   - User management                 │
└────────────┬────────────────────────┘
             │
             │ Workflows fetched by
             ↓
┌─────────────────────────────────────┐
│   User's Computer (CLI)             │
│   pip install zenthral-cli          │
│   - Executes workflows locally      │
│   - Uses their API keys             │
│   - Reports back to Railway         │
└─────────────────────────────────────┘
```

---

## 📁 What to Upload to Lovable

**Upload this entire folder:**
```
lovable-frontend/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── index.css
│   ├── components/
│   ├── pages/
│   ├── lib/
│   └── types/
└── public/
```

**Don't upload:**
- `/web/` - Goes to Railway
- `/zenthral-cli/` - Published to PyPI
- `/node_modules/` - Auto-generated

---

## ✅ Deployment Checklist

### Backend (Railway)
- [ ] Deploy `/web/` to Railway
- [ ] Add PostgreSQL database
- [ ] Set environment variables
- [ ] Copy backend URL

### Frontend (Lovable)
- [ ] Import `/lovable-frontend/` to Lovable
- [ ] Set `VITE_API_URL` environment variable
- [ ] Deploy and test

### CLI (PyPI)
- [ ] Test locally: `pip install -e zenthral-cli/`
- [ ] Publish to PyPI (when ready)

### Testing
- [ ] Register account in Lovable frontend
- [ ] Add API key in Settings
- [ ] Create test workflow
- [ ] Install CLI locally
- [ ] Run workflow with CLI

---

## 🆘 Troubleshooting

### "API calls failing from Lovable"
- Check `VITE_API_URL` is set correctly in Lovable env vars
- Verify Railway backend is running
- Check CORS settings in Flask app

### "Login not working"
- Check Railway database is created
- Run migrations: `railway run python -c "from app import app, db; app.app_context().push(); db.create_all()"`

### "Lovable can't find my code"
- Make sure you upload the `lovable-frontend` folder, not the root
- Check `package.json` exists in uploaded folder

---

## 🎉 You're Live!

After deployment:

1. **Frontend**: `https://your-project.lovable.app`
2. **Backend**: `https://zenthral-production.up.railway.app`
3. **CLI**: `pip install zenthral-cli` (when published)

**Share your Lovable URL** and start getting users!

---

## 📞 Need Help?

- **Lovable Support**: https://lovable.dev/docs
- **Railway Support**: https://railway.app/help
- **Your Backend Logs**: `railway logs`

**Your SaaS is ready to launch!** 🚀
