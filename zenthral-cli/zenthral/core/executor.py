"""
Workflow execution engine - runs workflows locally
"""
import os
import subprocess
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class WorkflowExecutor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.scripts_dir = Path(__file__).parent.parent.parent / 'scripts'

    def get_api_keys(self) -> Dict[str, str]:
        """Get AI provider API keys from environment or config"""
        return {
            'OPENAI_API_KEY': self.config.get('openai_api_key') or os.getenv('OPENAI_API_KEY'),
            'ANTHROPIC_API_KEY': self.config.get('anthropic_api_key') or os.getenv('ANTHROPIC_API_KEY'),
            'GOOGLE_API_KEY': self.config.get('google_api_key') or os.getenv('GOOGLE_API_KEY'),
            'GROQ_API_KEY': self.config.get('groq_api_key') or os.getenv('GROQ_API_KEY'),
        }

    def execute_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow and return results"""
        workflow_id = workflow.get('id')
        workflow_name = workflow.get('name')
        workflow_json = workflow.get('workflow_json', workflow)

        logger.info(f"Executing workflow: {workflow_name} ({workflow_id})")

        try:
            # Execute each action in the workflow
            results = []
            for action in workflow_json.get('actions', []):
                result = self.execute_action(action)
                results.append(result)

            return {
                'status': 'completed',
                'results': results,
                'logs': '\n'.join([r.get('output', '') for r in results])
            }

        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'logs': ''
            }

    def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single action"""
        action_type = action.get('type')

        logger.info(f"Executing action: {action_type}")

        if action_type == 'RUN_AGENT':
            return self.run_agent(action)
        elif action_type == 'SCRAPE_PAGE':
            return self.scrape_page(action)
        elif action_type == 'AI_ANALYZE':
            return self.ai_analyze(action)
        elif action_type == 'SEND_EMAIL':
            return self.send_email(action)
        else:
            logger.warning(f"Unknown action type: {action_type}")
            return {
                'status': 'skipped',
                'output': f'Unknown action type: {action_type}'
            }

    def run_agent(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Run a Python agent script"""
        agent_id = action.get('agent_id')
        parameters = action.get('parameters', {})

        # Find agent script
        agent_script = self.scripts_dir / f"{agent_id}.py"

        if not agent_script.exists():
            return {
                'status': 'failed',
                'error': f'Agent script not found: {agent_id}'
            }

        # Prepare environment with API keys
        env = os.environ.copy()
        env.update(self.get_api_keys())

        # Execute agent
        try:
            result = subprocess.run(
                ['python', str(agent_script)],
                env=env,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            return {
                'status': 'completed' if result.returncode == 0 else 'failed',
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None
            }

        except subprocess.TimeoutExpired:
            return {
                'status': 'failed',
                'error': 'Agent execution timed out'
            }
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }

    def scrape_page(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Scrape a web page"""
        import requests
        from bs4 import BeautifulSoup

        url = action.get('url')
        selector = action.get('selector')

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            if selector:
                elements = soup.select(selector)
                content = '\n'.join([el.get_text() for el in elements])
            else:
                content = soup.get_text()

            return {
                'status': 'completed',
                'output': content
            }

        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }

    def ai_analyze(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content with AI"""
        provider = action.get('provider', 'anthropic')
        model = action.get('model')
        prompt = action.get('prompt')

        api_keys = self.get_api_keys()

        try:
            if provider == 'anthropic':
                import anthropic
                client = anthropic.Anthropic(api_key=api_keys['ANTHROPIC_API_KEY'])
                response = client.messages.create(
                    model=model or 'claude-sonnet-4',
                    max_tokens=1024,
                    messages=[{'role': 'user', 'content': prompt}]
                )
                content = response.content[0].text
                tokens = response.usage.input_tokens + response.usage.output_tokens

            elif provider == 'openai':
                import openai
                client = openai.OpenAI(api_key=api_keys['OPENAI_API_KEY'])
                response = client.chat.completions.create(
                    model=model or 'gpt-4',
                    messages=[{'role': 'user', 'content': prompt}]
                )
                content = response.choices[0].message.content
                tokens = response.usage.total_tokens

            else:
                return {
                    'status': 'failed',
                    'error': f'Unknown AI provider: {provider}'
                }

            return {
                'status': 'completed',
                'output': content,
                'tokens_used': tokens
            }

        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }

    def send_email(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Send email"""
        # Placeholder - would integrate with user's email service
        return {
            'status': 'completed',
            'output': 'Email sending not yet implemented'
        }
