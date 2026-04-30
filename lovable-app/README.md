# Zenthral - Full Stack Next.js for Lovable

Everything you need to run Zenthral **100% in Lovable** with **zero other subscriptions**.

## 🚀 Quick Deploy

### 1. Set Up Supabase (Free)

1. Go to https://supabase.com
2. Create new project
3. Run the SQL from `supabase-schema.sql`
4. Copy your project URL and keys

### 2. Deploy to Lovable

1. Upload this entire folder to Lovable
2. Set environment variables (from Supabase)
3. Deploy!

**Total cost: $0/month** (or $20/month for custom domain)

## 📁 What's Inside

```
lovable-app/
├── app/                    # Next.js App Router
│   ├── page.tsx            # Home page
│   ├── layout.tsx          # Root layout
│   ├── dashboard/          # Dashboard page
│   ├── settings/           # Settings page
│   ├── create-automation/  # Workflow creator
│   └── api/                # API Routes (Serverless!)
│       ├── auth/           # Authentication
│       ├── workflows/      # Workflow CRUD
│       └── executions/     # Execution tracking
│
├── components/             # React components
├── lib/                    # Utilities
│   └── supabase.ts         # Supabase client
│
├── package.json
└── README.md               # This file
```

## 🎯 How It Works

- **Frontend**: Next.js pages (React)
- **Backend**: Next.js API routes (Serverless)
- **Database**: Supabase PostgreSQL (Free)
- **Auth**: Supabase Auth (Built-in)
- **Hosting**: Lovable (Free)

## 💰 Costs

- Lovable: **Free** (or $20/month for custom domain)
- Supabase: **Free** (500MB DB, 50K users)
- **Total: $0-20/month**

## 🔧 Local Development

```bash
npm install
npm run dev
```

Open http://localhost:3000

## 📚 More Info

See `LOVABLE_ONLY_DEPLOYMENT.md` for complete guide.

## ✅ Ready for Lovable

This folder is ready to upload to Lovable as-is!
