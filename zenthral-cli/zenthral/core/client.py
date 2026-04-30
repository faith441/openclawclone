"""
API client for communicating with Zenthral SaaS
"""
import requests
import os
from pathlib import Path
import yaml

class ZenthralClient:
    def __init__(self):
        self.config_path = Path.home() / '.zenthral' / 'config.yaml'
        self.config = self.load_config()
        self.api_url = self.config.get('api_url', 'https://api.zenthral.ai')
        self.api_key = self.config.get('api_key')

    def load_config(self):
        """Load configuration from ~/.zenthral/config.yaml"""
        if not self.config_path.exists():
            return {}

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f) or {}

    def save_config(self, config):
        """Save configuration to ~/.zenthral/config.yaml"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, 'w') as f:
            yaml.dump(config, f)

        self.config = config

    def _headers(self):
        """Get HTTP headers with auth"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def is_authenticated(self):
        """Check if user is authenticated"""
        return bool(self.api_key)

    # Auth endpoints
    def login(self, email, password):
        """Login to Zenthral SaaS"""
        response = requests.post(
            f'{self.api_url}/api/v1/auth/login',
            json={'email': email, 'password': password}
        )
        response.raise_for_status()
        return response.json()

    def me(self):
        """Get current user info"""
        response = requests.get(
            f'{self.api_url}/api/v1/auth/me',
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    # Workflow endpoints
    def get_pending_workflows(self):
        """Get workflows pending execution"""
        response = requests.get(
            f'{self.api_url}/api/v1/cli/workflows/pending',
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json().get('workflows', [])

    def get_workflow(self, workflow_id):
        """Get specific workflow"""
        response = requests.get(
            f'{self.api_url}/api/v1/workflows/{workflow_id}',
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def list_workflows(self):
        """List all workflows"""
        response = requests.get(
            f'{self.api_url}/api/v1/workflows',
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json().get('workflows', [])

    # Execution endpoints
    def report_execution_start(self, workflow_id):
        """Report that execution has started"""
        response = requests.post(
            f'{self.api_url}/api/v1/cli/executions',
            headers=self._headers(),
            json={
                'workflow_id': workflow_id,
                'status': 'running'
            }
        )
        response.raise_for_status()
        return response.json()

    def report_execution_complete(self, execution_id, status, logs=None, error=None, tokens=None, cost=None):
        """Report execution completion"""
        response = requests.put(
            f'{self.api_url}/api/v1/cli/executions/{execution_id}',
            headers=self._headers(),
            json={
                'status': status,
                'logs': logs,
                'error': error,
                'tokens_used': tokens,
                'cost': cost
            }
        )
        response.raise_for_status()
        return response.json()

    def send_logs(self, execution_id, logs):
        """Stream logs to SaaS"""
        response = requests.post(
            f'{self.api_url}/api/v1/cli/logs',
            headers=self._headers(),
            json={
                'execution_id': execution_id,
                'logs': logs
            }
        )
        response.raise_for_status()
        return response.json()
