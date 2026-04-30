export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
}

export interface Provider {
  id: string;
  name: string;
  description: string;
  models: string[];
  signup_url: string;
  local?: boolean;
}

export interface APIKey {
  id: string;
  provider: string;
  masked_key: string;
  is_active: boolean;
  created_at: string;
  last_used?: string;
}

export interface Preferences {
  default_provider?: string;
  default_model?: string;
  temperature: number;
  max_tokens: number;
  budget_limit?: number;
  budget_period: 'daily' | 'weekly' | 'monthly';
  auto_select_model: boolean;
}

export interface Workflow {
  name: string;
  description: string;
  trigger: {
    type: string;
    schedule?: string;
  };
  actions: Action[];
}

export interface Action {
  type: string;
  url?: string;
  prompt?: string;
  [key: string]: any;
}

export interface ActionBlock {
  type: string;
  name: string;
  description: string;
  parameters: Record<string, any>;
  example?: Record<string, any>;
}

export interface Agent {
  id: string;
  name: string;
  description: string;
  category: string;
  icon: string;
  author?: string;
  downloads?: number;
  rating?: number;
}

export interface Execution {
  id: string;
  agent_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  output?: string;
  error?: string;
  tokens_used?: number;
  cost?: number;
  created_at: string;
  completed_at?: string;
}
