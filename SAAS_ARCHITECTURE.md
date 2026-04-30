# Zenthral SaaS Architecture

## Overview

Zenthral is a multi-tenant SaaS platform where users design AI automation workflows in the cloud, but execution happens on their own infrastructure.

## Architecture Components

### 1. Cloud SaaS Platform (Your Infrastructure)

**Purpose**: Workflow designer, marketplace, user management
**Stack**: Flask (Python) + React (Lovable)
**Database**: PostgreSQL (multi-tenant)

**Responsibilities**:
- User authentication & authorization
- Workflow storage (JSON definitions)
- Marketplace catalog (agent templates)
- Team/workspace management
- Execution history & logs (reported by clients)
- Billing & usage tracking
- API for CLI clients

**Does NOT**:
- Execute workflows
- Store user's AI API keys (OpenAI, Anthropic, etc.)
- Run agents directly

### 2. Client Runtime (User's Infrastructure)

**Purpose**: Execute workflows locally using user's resources
**Stack**: Python CLI package
**Installation**: `pip install zenthral-cli`

**Responsibilities**:
- Authenticate with SaaS API
- Poll for workflows to execute
- Run agents locally using user's environment variables
- Use user's own AI API keys (from env vars)
- Report execution status/logs back to SaaS
- Can run as daemon/background service

**Runs on**:
- User's laptop (development)
- User's server (production)
- User's cloud (AWS/GCP/Azure)
- Docker container
- Kubernetes pod

### 3. Lovable Frontend

**Purpose**: Modern UI for workflow design
**Stack**: React + TypeScript + Tailwind
**Deployment**: Vercel/Netlify

**Features**:
- Workflow designer (drag-drop or natural language)
- Marketplace browser
- Dashboard (execution history)
- Team management
- Settings & billing

## Data Flow

### Workflow Creation
```
User → Lovable UI → SaaS API → Database (stores workflow JSON)
```

### Workflow Execution
```
1. User runs: `zenthral run` on their computer
2. CLI polls: GET /api/v1/workflows/pending
3. SaaS returns: Workflow JSON
4. CLI executes: Runs agents locally
5. CLI reports: POST /api/v1/executions (status, logs, cost)
6. User views: Dashboard in Lovable UI
```

## Database Schema (Multi-Tenant)

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    name VARCHAR,
    created_at TIMESTAMP,
    subscription_tier VARCHAR  -- free, pro, enterprise
);
```

### Workspaces Table (Multi-tenancy)
```sql
CREATE TABLE workspaces (
    id UUID PRIMARY KEY,
    name VARCHAR NOT NULL,
    owner_id UUID REFERENCES users(id),
    created_at TIMESTAMP
);
```

### Workflows Table
```sql
CREATE TABLE workflows (
    id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(id),
    name VARCHAR NOT NULL,
    description TEXT,
    workflow_json JSONB NOT NULL,  -- Full workflow definition
    trigger_type VARCHAR,  -- manual, schedule, webhook
    trigger_config JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### API Keys Table (For SaaS Access)
```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(id),
    key_hash VARCHAR NOT NULL,  -- Hashed API key for CLI auth
    name VARCHAR,  -- User-friendly name
    last_used TIMESTAMP,
    created_at TIMESTAMP
);
```

### Executions Table (History/Logs)
```sql
CREATE TABLE executions (
    id UUID PRIMARY KEY,
    workflow_id UUID REFERENCES workflows(id),
    workspace_id UUID REFERENCES workspaces(id),
    status VARCHAR,  -- pending, running, completed, failed
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    logs TEXT,
    error TEXT,
    tokens_used INTEGER,
    cost DECIMAL(10, 6),
    metadata JSONB  -- User-reported data
);
```

### Marketplace Agents Table
```sql
CREATE TABLE marketplace_agents (
    id UUID PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    category VARCHAR,
    template_json JSONB,  -- Workflow template
    author_id UUID REFERENCES users(id),
    downloads INTEGER DEFAULT 0,
    rating DECIMAL(3, 2),
    created_at TIMESTAMP
);
```

## API Endpoints

### SaaS Backend API

#### Authentication
- `POST /api/v1/auth/register` - Create account
- `POST /api/v1/auth/login` - Get JWT
- `GET /api/v1/auth/me` - Current user

#### Workspaces
- `GET /api/v1/workspaces` - List user's workspaces
- `POST /api/v1/workspaces` - Create workspace
- `GET /api/v1/workspaces/:id/api-keys` - Get API keys for CLI

#### Workflows
- `GET /api/v1/workflows` - List workflows
- `POST /api/v1/workflows` - Create workflow
- `GET /api/v1/workflows/:id` - Get workflow
- `PUT /api/v1/workflows/:id` - Update workflow
- `DELETE /api/v1/workflows/:id` - Delete workflow

#### CLI Endpoints (Used by zenthral-cli)
- `GET /api/v1/cli/workflows/pending` - Get workflows to execute
- `POST /api/v1/cli/executions` - Report execution status
- `POST /api/v1/cli/logs` - Stream logs

#### Marketplace
- `GET /api/v1/marketplace/agents` - Browse agents
- `GET /api/v1/marketplace/agents/:id` - Get agent template
- `POST /api/v1/marketplace/agents/:id/install` - Add to workspace

#### Executions (Read-only, populated by CLI)
- `GET /api/v1/executions` - List execution history
- `GET /api/v1/executions/:id` - Get execution details
- `GET /api/v1/executions/stats` - Usage statistics

## CLI Commands

### Installation
```bash
pip install zenthral-cli
```

### Authentication
```bash
# Login to SaaS
zenthral login

# Or use API key
zenthral login --api-key=zth_xxxxxxxxxxxxx
```

### Configuration
```bash
# Configure AI provider keys (stored locally only)
export OPENAI_API_KEY=sk-xxxxx
export ANTHROPIC_API_KEY=sk-ant-xxxxx

# Or use zenthral config
zenthral config set OPENAI_API_KEY sk-xxxxx
```

### Running Workflows
```bash
# Run once (execute pending workflows)
zenthral run

# Run as daemon (continuous polling)
zenthral daemon start

# Run specific workflow
zenthral run --workflow-id=abc123

# List local workflows
zenthral list
```

### Development
```bash
# Test workflow locally
zenthral test workflow.json

# View logs
zenthral logs

# Check status
zenthral status
```

## Security Model

### User's AI API Keys
- **NEVER** stored in SaaS database
- Stored locally on user's machine (env vars or config file)
- Used only during local execution
- Never transmitted to SaaS platform

### SaaS API Keys
- Generated by SaaS for CLI authentication
- Format: `zth_xxxxxxxxxxxxxxxx`
- Stored in `~/.zenthral/config`
- Used to authenticate CLI → SaaS requests

### Workflow Data
- Stored in SaaS database (encrypted at rest)
- User owns their workflow definitions
- Can export/import workflows
- GDPR compliant (user can delete all data)

## Deployment

### SaaS Backend
- **Platform**: Railway, Render, or Fly.io
- **Database**: Managed PostgreSQL
- **Cost**: ~$20-50/month

### Frontend
- **Platform**: Vercel (free tier)
- **Build**: Automatic from GitHub
- **CDN**: Global edge network

### CLI Distribution
- **PyPI**: `pip install zenthral-cli`
- **GitHub Releases**: Binary distributions
- **Docker**: `docker run zenthral/cli`

## Monetization

### Free Tier
- 1 workspace
- 100 executions/month
- Community marketplace access

### Pro Tier ($29/month)
- Unlimited workspaces
- Unlimited executions
- Priority support
- Private marketplace

### Enterprise Tier ($299/month)
- Everything in Pro
- Team management
- SSO/SAML
- SLA guarantees
- Dedicated support

## Benefits of This Architecture

✅ **Users control their infrastructure** - Runs on their servers
✅ **Users own their API keys** - No middleman markup
✅ **Scalable** - Users scale their own execution
✅ **Cost-effective** - You only host the UI/API, not execution
✅ **Secure** - User's keys never leave their environment
✅ **Flexible** - Works on laptop, server, or cloud
✅ **Privacy** - User data never processed by your servers

This is exactly how **n8n**, **Temporal**, and **Prefect** work!
