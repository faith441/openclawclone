-- Zenthral Database Schema for Supabase
-- Run this in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (Supabase Auth handles this, but we add metadata)
CREATE TABLE public.user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    name VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Workspaces table
CREATE TABLE public.workspaces (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL,
    owner_id UUID REFERENCES auth.users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Workflows table
CREATE TABLE public.workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID REFERENCES public.workspaces(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    description TEXT,
    workflow_json JSONB NOT NULL,
    trigger_type VARCHAR DEFAULT 'manual',
    trigger_config JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Executions table
CREATE TABLE public.executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID REFERENCES public.workflows(id) ON DELETE CASCADE,
    workspace_id UUID REFERENCES public.workspaces(id) ON DELETE CASCADE,
    status VARCHAR DEFAULT 'pending',
    logs TEXT,
    error TEXT,
    tokens_used INTEGER,
    cost DECIMAL(10, 6),
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    metadata JSONB
);

-- API Keys table (for CLI authentication)
CREATE TABLE public.api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID REFERENCES public.workspaces(id) ON DELETE CASCADE,
    key_prefix VARCHAR(10) NOT NULL,
    key_hash VARCHAR NOT NULL,
    name VARCHAR,
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- User AI Keys table (for cloud execution mode - encrypted storage)
CREATE TABLE public.user_ai_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL, -- 'openai', 'anthropic', 'google', 'groq'
    encrypted_key TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    last_tested TIMESTAMP,
    test_status VARCHAR(20), -- 'valid', 'invalid', 'not_tested'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, provider)
);

-- Installed Skills table (tracks which skills users have installed)
CREATE TABLE public.installed_skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    skill_id VARCHAR NOT NULL,
    skill_name VARCHAR NOT NULL,
    execution_mode VARCHAR(20) DEFAULT 'cloud', -- 'cloud' or 'local'
    is_enabled BOOLEAN DEFAULT true,
    config JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, skill_id)
);

-- Row Level Security (RLS) Policies

-- Enable RLS
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workspaces ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workflows ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.executions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_ai_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.installed_skills ENABLE ROW LEVEL SECURITY;

-- User profiles: users can only see their own
CREATE POLICY "Users can view own profile"
    ON public.user_profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON public.user_profiles FOR UPDATE
    USING (auth.uid() = id);

-- Workspaces: users can only see their own workspaces
CREATE POLICY "Users can view own workspaces"
    ON public.workspaces FOR SELECT
    USING (auth.uid() = owner_id);

CREATE POLICY "Users can create workspaces"
    ON public.workspaces FOR INSERT
    WITH CHECK (auth.uid() = owner_id);

CREATE POLICY "Users can update own workspaces"
    ON public.workspaces FOR UPDATE
    USING (auth.uid() = owner_id);

-- Workflows: users can only see workflows in their workspaces
CREATE POLICY "Users can view workflows in their workspaces"
    ON public.workflows FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.workspaces
            WHERE workspaces.id = workflows.workspace_id
            AND workspaces.owner_id = auth.uid()
        )
    );

CREATE POLICY "Users can create workflows in their workspaces"
    ON public.workflows FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.workspaces
            WHERE workspaces.id = workflows.workspace_id
            AND workspaces.owner_id = auth.uid()
        )
    );

CREATE POLICY "Users can update workflows in their workspaces"
    ON public.workflows FOR UPDATE
    USING (
        EXISTS (
            SELECT 1 FROM public.workspaces
            WHERE workspaces.id = workflows.workspace_id
            AND workspaces.owner_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete workflows in their workspaces"
    ON public.workflows FOR DELETE
    USING (
        EXISTS (
            SELECT 1 FROM public.workspaces
            WHERE workspaces.id = workflows.workspace_id
            AND workspaces.owner_id = auth.uid()
        )
    );

-- Executions: users can view executions in their workspaces
CREATE POLICY "Users can view executions in their workspaces"
    ON public.executions FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.workspaces
            WHERE workspaces.id = executions.workspace_id
            AND workspaces.owner_id = auth.uid()
        )
    );

CREATE POLICY "Users can create executions"
    ON public.executions FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.workspaces
            WHERE workspaces.id = executions.workspace_id
            AND workspaces.owner_id = auth.uid()
        )
    );

-- API Keys: users can view API keys in their workspaces
CREATE POLICY "Users can view API keys in their workspaces"
    ON public.api_keys FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.workspaces
            WHERE workspaces.id = api_keys.workspace_id
            AND workspaces.owner_id = auth.uid()
        )
    );

CREATE POLICY "Users can create API keys"
    ON public.api_keys FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.workspaces
            WHERE workspaces.id = api_keys.workspace_id
            AND workspaces.owner_id = auth.uid()
        )
    );

-- User AI Keys: users can only see their own AI keys
CREATE POLICY "Users can view own AI keys"
    ON public.user_ai_keys FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own AI keys"
    ON public.user_ai_keys FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own AI keys"
    ON public.user_ai_keys FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own AI keys"
    ON public.user_ai_keys FOR DELETE
    USING (auth.uid() = user_id);

-- Installed Skills: users can only see their own installed skills
CREATE POLICY "Users can view own installed skills"
    ON public.installed_skills FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can install skills"
    ON public.installed_skills FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own installed skills"
    ON public.installed_skills FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own installed skills"
    ON public.installed_skills FOR DELETE
    USING (auth.uid() = user_id);

-- Indexes for better performance
CREATE INDEX idx_workspaces_owner ON public.workspaces(owner_id);
CREATE INDEX idx_workflows_workspace ON public.workflows(workspace_id);
CREATE INDEX idx_executions_workflow ON public.executions(workflow_id);
CREATE INDEX idx_executions_workspace ON public.executions(workspace_id);
CREATE INDEX idx_api_keys_workspace ON public.api_keys(workspace_id);
CREATE INDEX idx_user_ai_keys_user ON public.user_ai_keys(user_id);
CREATE INDEX idx_user_ai_keys_provider ON public.user_ai_keys(user_id, provider);
CREATE INDEX idx_installed_skills_user ON public.installed_skills(user_id);
CREATE INDEX idx_installed_skills_skill ON public.installed_skills(skill_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers to auto-update updated_at
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON public.user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workspaces_updated_at BEFORE UPDATE ON public.workspaces
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workflows_updated_at BEFORE UPDATE ON public.workflows
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_ai_keys_updated_at BEFORE UPDATE ON public.user_ai_keys
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_installed_skills_updated_at BEFORE UPDATE ON public.installed_skills
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
