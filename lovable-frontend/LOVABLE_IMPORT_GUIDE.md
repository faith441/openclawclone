# Zenthral Frontend - Lovable Import Guide

This is a complete React/TypeScript frontend for the Zenthral AI Automation Platform that connects to your existing Python backend.

## Quick Setup

### 1. Import to Lovable

You can import this entire `lovable-frontend` directory to Lovable in one of these ways:

**Option A: Direct Import**
1. Open Lovable.dev
2. Create a new project
3. Use "Import from GitHub" or "Import from Files"
4. Upload this entire directory

**Option B: Manual Setup**
1. Create a new Vite + React + TypeScript project in Lovable
2. Copy all files from this directory into your Lovable project
3. Lovable will auto-install dependencies

### 2. Configure Backend URL

Create a `.env` file in the root:

```env
VITE_API_URL=http://localhost:5001
```

For production, point this to your deployed Python backend (e.g., Railway, Render, Fly.io).

### 3. Run Frontend

```bash
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`

### 4. Keep Python Backend Running

Your Python backend continues to run separately:

```bash
cd /Users/faithtemporosa/openclawclone/openclawclone/web
source venv/bin/activate
python app.py
```

Backend runs on `http://localhost:5001`

## Project Structure

```
lovable-frontend/
├── src/
│   ├── components/
│   │   └── Layout.tsx          # Main app layout with sidebar
│   ├── pages/
│   │   ├── LoginPage.tsx       # Authentication
│   │   ├── RegisterPage.tsx
│   │   ├── DashboardPage.tsx   # Overview & stats
│   │   ├── SettingsPage.tsx    # API key management (BYOK)
│   │   ├── CreateAutomationPage.tsx  # Natural language → workflows
│   │   ├── SkillsPage.tsx      # Agent marketplace
│   │   └── AgentsPage.tsx      # Installed agents
│   ├── lib/
│   │   ├── api.ts              # API client for Python backend
│   │   └── utils.ts            # Helper functions
│   ├── types/
│   │   └── index.ts            # TypeScript types
│   ├── App.tsx                 # Main app & routing
│   ├── main.tsx               # Entry point
│   └── index.css              # Tailwind styles
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Key Features

### 1. **BYOK (Bring Your Own Key)**
- Settings page for managing API keys
- Supports OpenAI, Anthropic, Google, Groq, Ollama
- Keys encrypted in Python backend
- No vendor lock-in

### 2. **Natural Language Automation**
- Type what you want in plain English
- AI generates executable workflows
- Visual workflow preview
- One-click deployment

### 3. **Agent Marketplace**
- Browse & install agents
- Run agents with custom parameters
- Track executions & costs
- View agent history

### 4. **Full Python Integration**
- All your existing Python agents work unchanged
- Execution engine stays in Python
- AI Router & Workflow Engine in Python
- Frontend just calls REST APIs

## API Endpoints Used

The frontend connects to these Python backend endpoints:

### Authentication
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/register`
- `GET /api/v1/auth/me`

### API Keys
- `GET /api/v1/api-keys/providers`
- `GET /api/v1/api-keys/`
- `POST /api/v1/api-keys/`
- `DELETE /api/v1/api-keys/{id}`
- `POST /api/v1/api-keys/{id}/toggle`
- `GET /api/v1/api-keys/preferences`
- `PUT /api/v1/api-keys/preferences`

### Workflows
- `POST /api/v1/workflows/generate`
- `POST /api/v1/workflows/validate`
- `GET /api/v1/workflows/action-blocks`
- `POST /api/v1/workflows/test`
- `POST /api/v1/workflows/chat`

### Agents
- `GET /api/v1/agents/catalog`
- `GET /api/v1/agents/installed`
- `POST /api/v1/agents/{id}/install`
- `DELETE /api/v1/agents/{id}`

### Executions
- `POST /api/v1/executions/run`
- `GET /api/v1/executions/{id}`
- `GET /api/v1/executions/history`
- `GET /api/v1/executions/stats`

## Deployment

### Frontend (Vercel/Netlify)

1. Push to GitHub
2. Connect to Vercel/Netlify
3. Set environment variable: `VITE_API_URL=https://your-backend.railway.app`
4. Deploy!

### Backend (Railway/Render/Fly.io)

Your Python backend can stay where it is or deploy to:

**Railway:**
```bash
railway init
railway up
```

**Render:**
- Create new Web Service
- Connect GitHub repo
- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`

**Fly.io:**
```bash
fly launch
fly deploy
```

## Hybrid Architecture Benefits

✅ **Your Python agents continue to work** - Zero changes needed
✅ **Modern React UI** - Built with Lovable, looks professional
✅ **Easy deployment** - Frontend and backend deploy separately
✅ **Scalable** - Scale frontend (static) and backend (compute) independently
✅ **Cost-effective** - Frontend is free on Vercel, backend cheap on Railway

## Development Workflow

1. **Frontend dev**: `npm run dev` (port 3000)
2. **Backend dev**: `python app.py` (port 5001)
3. Vite proxy forwards `/api/*` requests to backend
4. Hot reload on both sides

## Customization in Lovable

Once imported to Lovable, you can easily customize:

- **Colors**: Edit `tailwind.config.js` or use Lovable's theme editor
- **Components**: Ask Lovable to modify any component
- **Pages**: Add new pages by asking Lovable
- **API integration**: All in `src/lib/api.ts`, easy to extend

## Support

Need help? The frontend is fully typed with TypeScript, so Lovable will understand it perfectly. Just ask Lovable to:

- "Add a new page for X"
- "Change the color scheme to dark mode"
- "Add a new feature to the Settings page"
- "Create a new API integration for Y"

Lovable will handle it seamlessly!

---

**You now have a production-ready SaaS frontend that works with your existing Python backend!** 🎉
