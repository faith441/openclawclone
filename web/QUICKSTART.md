# Zenthral AI Platform - Quick Start Guide

## ✅ Issues Fixed

1. **Import errors** - Added graceful fallback for missing modules
2. **API blueprint** - Created proper routing structure
3. **Database initialization** - Added error handling
4. **Dependencies** - Added pyyaml to requirements
5. **Diagnostic tools** - Created fix_imports.py and test_system.sh

---

## 🚀 Quick Start (3 Steps)

### Step 1: Run Setup

```bash
cd /Users/faithtemporosa/openclawclone/openclawclone/web
./setup.sh
```

This will:
- Install all Python dependencies
- Create .env file with secure secrets
- Initialize SQLite database
- Create all tables (users, organizations, agent_catalog, etc.)

### Step 2: Start Server

```bash
python3 app.py
```

You should see:
```
⚡ Zenthral AI Platform - SaaS Edition
🚀 Starting web dashboard...
📍 URL: http://localhost:5001
✓ Database initialized
```

### Step 3: Register Account

Open: **http://localhost:5001/auth/register**

Create your account:
- Full Name: Your Name
- Email: your@email.com
- Password: Must have uppercase, lowercase, and number (e.g., TestPass123!)

---

## 🧪 Testing (Optional)

Run the test suite before starting:

```bash
./test_system.sh
```

This validates:
- All Python imports work
- Database can be created
- Flask app configuration is correct

---

## 🐛 Troubleshooting

### Issue: "Module not found"

**Fix:**
```bash
./setup.sh
```

### Issue: "Port 5001 already in use"

**Fix:**
```bash
# Kill existing process
lsof -ti:5001 | xargs kill -9

# Or change port in app.py (last line)
```

### Issue: Import errors

**Diagnose:**
```bash
python3 fix_imports.py
```

This will show which modules are missing and why.

### Issue: Database errors

**Fix:**
```bash
# Remove and recreate
rm zenthral.db
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

---

## 📝 What Works Now

### ✅ Phase 1: Authentication (100%)
- User registration with email verification
- Login with JWT tokens (15min access, 30 day refresh)
- Password reset flow
- Protected API endpoints
- Multi-tenant organizations
- Role-based access control

### ✅ Database Models
- **users** - Authentication and profiles
- **organizations** - Workspaces for multi-tenancy
- **organization_members** - Team membership
- **agent_catalog** - Available agents (ready for Phase 2)
- **installed_agents** - User's installed agents (ready for Phase 2)

### ✅ REST API
All endpoints at `/api/v1/auth/*`:
- POST `/register` - Create account
- POST `/login` - Get JWT tokens
- POST `/verify-email` - Verify email
- POST `/forgot-password` - Request reset
- POST `/reset-password` - Reset password
- POST `/refresh` - Refresh access token
- GET `/me` - Get current user (requires auth)

---

## 📚 API Examples

### Register
```bash
curl -X POST http://localhost:5001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!",
    "full_name": "Test User"
  }'
```

### Login
```bash
curl -X POST http://localhost:5001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'
```

### Get Current User (with token)
```bash
curl http://localhost:5001/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🔐 Security Features

- **Passwords**: Bcrypt hashing with 12 rounds
- **Tokens**: JWT with short-lived access tokens
- **Database**: UUID primary keys
- **Encryption**: AES-256 for sensitive data (ready)
- **Email verification**: Required before login
- **CORS**: Configurable for production

---

## 📁 File Structure

```
web/
├── app.py                      # Main Flask application
├── config.py                   # Configuration management
├── setup.sh                    # Automated setup script
├── test_system.sh              # Test suite
├── fix_imports.py              # Diagnostic tool
├── .env                        # Environment variables (generated)
├── zenthral.db                 # SQLite database (generated)
│
├── models/                     # Database models
│   ├── __init__.py
│   ├── user.py                 # User, Organization
│   └── agent.py                # AgentCatalog, InstalledAgent
│
├── services/                   # Business logic
│   └── auth_service.py         # Authentication
│
├── utils/                      # Utilities
│   ├── jwt_utils.py            # JWT tokens
│   ├── email.py                # Email sending
│   └── encryption.py           # API key encryption
│
├── api/                        # REST API
│   ├── __init__.py
│   └── v1/
│       └── auth.py             # Auth endpoints
│
├── middleware/                 # Request middleware
│   └── auth_middleware.py      # JWT verification
│
└── templates/                  # HTML pages
    └── auth/
        ├── login.html
        ├── register.html
        └── verify_email.html
```

---

## 🎯 Next Steps

### Option 1: Test What's Built
- Create an account
- Test login
- Try the API endpoints
- Explore the database

### Option 2: Continue Phase 2
- Agent Marketplace UI
- Browse/install agents
- Agent configuration
- Encryption for API keys

### Option 3: Jump to Phase 3
- Execution Engine
- Run agents
- Track usage
- Cost calculation

---

## 💡 Tips

1. **Email verification**: In development, verification emails print to console (no SMTP needed)
2. **Database**: Currently using SQLite - easy to switch to PostgreSQL later
3. **Tokens**: Store access_token in localStorage or cookies for web apps
4. **API keys**: Will be encrypted when stored in agent configurations
5. **Debugging**: All errors print to console with stack traces

---

## 🆘 Need Help?

1. **Check imports**: `python3 fix_imports.py`
2. **Run tests**: `./test_system.sh`
3. **View logs**: Check terminal output when running `python3 app.py`
4. **Reset database**: `rm zenthral.db && ./setup.sh`

---

**You're all set! Run `./setup.sh` to begin.** 🚀
