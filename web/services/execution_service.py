"""
Execution Service
Handles running agents and tracking execution history
"""
import os
import sys
import json
import subprocess
import threading
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import db
from models.execution import Execution, UsageSummary
from models.agent import InstalledAgent, AgentCatalog
from utils.encryption import decrypt_dict


# Cost per 1K tokens (approximate, varies by model)
COST_PER_1K_TOKENS = {
    'gpt-4': {'input': 0.03, 'output': 0.06},
    'gpt-4-turbo': {'input': 0.01, 'output': 0.03},
    'gpt-3.5-turbo': {'input': 0.0005, 'output': 0.0015},
    'claude-3-opus': {'input': 0.015, 'output': 0.075},
    'claude-3-sonnet': {'input': 0.003, 'output': 0.015},
    'claude-3-haiku': {'input': 0.00025, 'output': 0.00125},
    'default': {'input': 0.01, 'output': 0.03}
}


class ExecutionService:
    """Service for executing agents and tracking history"""

    @staticmethod
    def run_agent(
        user_id: str,
        installed_agent_id: str,
        input_data: Dict,
        model_name: str = 'default'
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Run an installed agent with the given input

        Args:
            user_id: User ID
            installed_agent_id: ID of the installed agent
            input_data: Input parameters for the agent
            model_name: AI model to use

        Returns:
            Tuple of (execution_dict, error_message)
        """
        # Get installed agent
        installed_agent = InstalledAgent.query.filter_by(
            id=installed_agent_id,
            user_id=user_id
        ).first()

        if not installed_agent:
            return None, 'Agent not found or not installed'

        if not installed_agent.is_enabled:
            return None, 'Agent is disabled'

        # Get agent catalog info
        agent = installed_agent.agent
        if not agent:
            return None, 'Agent catalog entry not found'

        # Create execution record
        execution = Execution.create(
            user_id=user_id,
            installed_agent_id=installed_agent_id,
            input_data=input_data,
            status='pending',
            model_name=model_name
        )

        # Start execution in background thread
        thread = threading.Thread(
            target=ExecutionService._execute_agent,
            args=(execution.id, installed_agent, agent, input_data)
        )
        thread.start()

        return execution.to_dict(), None

    @staticmethod
    def _execute_agent(
        execution_id: str,
        installed_agent: InstalledAgent,
        agent: AgentCatalog,
        input_data: Dict
    ):
        """Execute agent in background thread"""
        from app import app

        with app.app_context():
            execution = Execution.query.get(execution_id)
            if not execution:
                return

            # Mark as running
            execution.start()

            try:
                # Get decrypted configuration
                config = {}
                if installed_agent.config_json:
                    config = decrypt_dict(installed_agent.config_json)

                # Build environment variables
                env = os.environ.copy()
                env.update(config)
                env['AGENT_INPUT'] = json.dumps(input_data)
                env['AGENT_NAME'] = agent.name
                env['AGENT_ID'] = agent.id

                # Get script path
                script_path = Path(__file__).parent.parent.parent / agent.file_path

                if not script_path.exists():
                    execution.fail(f'Agent script not found: {agent.file_path}')
                    return

                # Run the agent script
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minute timeout
                    cwd=str(script_path.parent)
                )

                if result.returncode == 0:
                    # Parse output
                    output = result.stdout.strip()

                    # Try to parse as JSON
                    try:
                        output_data = json.loads(output)
                    except json.JSONDecodeError:
                        output_data = {'result': output}

                    # Estimate tokens (rough approximation)
                    input_text = json.dumps(input_data)
                    output_text = output
                    input_tokens = len(input_text.split()) * 2  # Rough estimate
                    output_tokens = len(output_text.split()) * 2

                    # Calculate cost
                    model_costs = COST_PER_1K_TOKENS.get(
                        execution.model_name,
                        COST_PER_1K_TOKENS['default']
                    )
                    cost = (
                        (input_tokens / 1000) * model_costs['input'] +
                        (output_tokens / 1000) * model_costs['output']
                    )

                    execution.complete(
                        output_data=output_data,
                        tokens={'input': input_tokens, 'output': output_tokens},
                        cost=cost
                    )

                    # Update usage summary
                    ExecutionService._update_usage_summary(
                        execution.user_id,
                        input_tokens,
                        output_tokens,
                        cost,
                        success=True
                    )

                else:
                    error_msg = result.stderr or 'Agent execution failed'
                    execution.fail(error_msg)

                    # Update usage summary
                    ExecutionService._update_usage_summary(
                        execution.user_id,
                        0, 0, 0,
                        success=False
                    )

            except subprocess.TimeoutExpired:
                execution.fail('Agent execution timed out (5 minute limit)')
            except Exception as e:
                execution.fail(f'Execution error: {str(e)}')

    @staticmethod
    def _update_usage_summary(
        user_id: str,
        input_tokens: int,
        output_tokens: int,
        cost: float,
        success: bool
    ):
        """Update daily usage summary"""
        today = datetime.utcnow().date()

        summary = UsageSummary.query.filter_by(
            user_id=user_id,
            date=today
        ).first()

        if not summary:
            summary = UsageSummary.create(
                user_id=user_id,
                date=today,
                total_executions=0,
                successful_executions=0,
                failed_executions=0,
                total_input_tokens=0,
                total_output_tokens=0,
                total_tokens=0,
                total_cost_usd=0.0
            )

        summary.total_executions += 1
        if success:
            summary.successful_executions += 1
        else:
            summary.failed_executions += 1

        summary.total_input_tokens += input_tokens
        summary.total_output_tokens += output_tokens
        summary.total_tokens += (input_tokens + output_tokens)
        summary.total_cost_usd += cost

        db.session.commit()

    @staticmethod
    def get_execution(user_id: str, execution_id: str) -> Optional[Dict]:
        """Get execution by ID"""
        execution = Execution.query.filter_by(
            id=execution_id,
            user_id=user_id
        ).first()

        if not execution:
            return None

        result = execution.to_dict()

        # Add agent info
        if execution.installed_agent and execution.installed_agent.agent:
            result['agent_info'] = {
                'name': execution.installed_agent.agent.name,
                'icon': execution.installed_agent.agent.icon
            }

        return result

    @staticmethod
    def get_user_executions(
        user_id: str,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None
    ) -> Tuple[List[Dict], int]:
        """Get user's execution history"""
        query = Execution.query.filter_by(user_id=user_id)

        if status:
            query = query.filter_by(status=status)

        total = query.count()

        executions = query.order_by(
            Execution.created_at.desc()
        ).limit(limit).offset(offset).all()

        result = []
        for execution in executions:
            data = execution.to_dict()
            if execution.installed_agent and execution.installed_agent.agent:
                data['agent_info'] = {
                    'name': execution.installed_agent.agent.name,
                    'icon': execution.installed_agent.agent.icon
                }
            result.append(data)

        return result, total

    @staticmethod
    def get_usage_stats(user_id: str, days: int = 30) -> Dict:
        """Get usage statistics for a user"""
        from datetime import timedelta

        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)

        summaries = UsageSummary.query.filter(
            UsageSummary.user_id == user_id,
            UsageSummary.date >= start_date,
            UsageSummary.date <= end_date
        ).all()

        total_executions = sum(s.total_executions for s in summaries)
        successful = sum(s.successful_executions for s in summaries)
        failed = sum(s.failed_executions for s in summaries)
        total_tokens = sum(s.total_tokens for s in summaries)
        total_cost = sum(s.total_cost_usd for s in summaries)

        return {
            'period_days': days,
            'total_executions': total_executions,
            'successful_executions': successful,
            'failed_executions': failed,
            'success_rate': (successful / total_executions * 100) if total_executions > 0 else 0,
            'total_tokens': total_tokens,
            'total_cost_usd': round(total_cost, 4),
            'daily_breakdown': [s.to_dict() for s in summaries]
        }


# Convenience functions
def run_agent(user_id: str, installed_agent_id: str, input_data: Dict, model_name: str = 'default'):
    """Run an agent"""
    return ExecutionService.run_agent(user_id, installed_agent_id, input_data, model_name)


def get_execution(user_id: str, execution_id: str):
    """Get execution details"""
    return ExecutionService.get_execution(user_id, execution_id)


def get_user_executions(user_id: str, limit: int = 50, offset: int = 0, status: str = None):
    """Get user's execution history"""
    return ExecutionService.get_user_executions(user_id, limit, offset, status)


def get_usage_stats(user_id: str, days: int = 30):
    """Get usage statistics"""
    return ExecutionService.get_usage_stats(user_id, days)
