"""
Agent Marketplace Service
Handles agent discovery, installation, and configuration
"""
import os
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import db
from models.agent import AgentCatalog, InstalledAgent
from models.user import User
from utils.encryption import encrypt_dict, decrypt_dict


class AgentService:
    """Service for managing agent marketplace operations"""

    @staticmethod
    def browse_agents(
        category: Optional[str] = None,
        search_query: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[Dict], int]:
        """
        Browse available agents in the marketplace

        Args:
            category: Filter by category (e.g., 'finance', 'healthcare')
            search_query: Search in name and description
            limit: Max results to return
            offset: Pagination offset

        Returns:
            Tuple of (agent_list, total_count)
        """
        query = AgentCatalog.query.filter_by(is_active=True)

        # Apply filters
        if category:
            query = query.filter_by(category=category)

        if search_query:
            search_pattern = f'%{search_query}%'
            query = query.filter(
                db.or_(
                    AgentCatalog.name.ilike(search_pattern),
                    AgentCatalog.description.ilike(search_pattern)
                )
            )

        # Get total count
        total_count = query.count()

        # Apply pagination and ordering
        agents = query.order_by(
            AgentCatalog.install_count.desc(),
            AgentCatalog.rating.desc()
        ).limit(limit).offset(offset).all()

        # Convert to dict
        agent_list = [agent.to_dict() for agent in agents]

        return agent_list, total_count

    @staticmethod
    def get_agent_detail(agent_id: str) -> Optional[Dict]:
        """Get detailed information about a specific agent"""
        agent = AgentCatalog.query.filter_by(id=agent_id, is_active=True).first()
        if not agent:
            return None

        return agent.to_dict()

    @staticmethod
    def get_categories() -> List[Dict[str, any]]:
        """Get all available agent categories with counts"""
        categories = db.session.query(
            AgentCatalog.category,
            db.func.count(AgentCatalog.id).label('count')
        ).filter_by(is_active=True).group_by(AgentCatalog.category).all()

        return [
            {'name': cat, 'count': count}
            for cat, count in categories
        ]

    @staticmethod
    def install_agent(user_id: str, agent_id: str, config: Optional[Dict] = None) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Install an agent for a user

        Args:
            user_id: User ID
            agent_id: Agent catalog ID
            config: Initial configuration (optional)

        Returns:
            Tuple of (installed_agent_dict, error_message)
        """
        # Check if agent exists
        agent = AgentCatalog.query.filter_by(id=agent_id, is_active=True).first()
        if not agent:
            return None, 'Agent not found'

        # Check if already installed
        existing = InstalledAgent.query.filter_by(
            user_id=user_id,
            agent_id=agent_id
        ).first()

        if existing:
            return None, 'Agent already installed'

        # Validate required environment variables if config provided
        if config and agent.env_vars_required:
            missing_vars = []
            for var in agent.env_vars_required:
                if var not in config:
                    missing_vars.append(var)

            if missing_vars:
                return None, f'Missing required configuration: {", ".join(missing_vars)}'

        # Encrypt sensitive configuration
        encrypted_config = None
        if config:
            encrypted_config = encrypt_dict(config)

        # Create installed agent
        installed_agent = InstalledAgent.create(
            user_id=user_id,
            agent_id=agent_id,
            config_json=encrypted_config,
            is_enabled=True
        )

        # Increment install count
        agent.install_count += 1
        db.session.commit()

        return installed_agent.to_dict(), None

    @staticmethod
    def uninstall_agent(user_id: str, installed_agent_id: str) -> Tuple[bool, Optional[str]]:
        """
        Uninstall an agent

        Returns:
            Tuple of (success, error_message)
        """
        installed_agent = InstalledAgent.query.filter_by(
            id=installed_agent_id,
            user_id=user_id
        ).first()

        if not installed_agent:
            return False, 'Installed agent not found'

        # Delete
        db.session.delete(installed_agent)
        db.session.commit()

        return True, None

    @staticmethod
    def get_user_installed_agents(user_id: str) -> List[Dict]:
        """Get all agents installed by a user"""
        installed_agents = InstalledAgent.query.filter_by(user_id=user_id).all()

        result = []
        for installed in installed_agents:
            data = installed.to_dict()

            # Add agent catalog info
            if installed.agent:
                data['agent_info'] = {
                    'name': installed.agent.name,
                    'slug': installed.agent.slug,
                    'description': installed.agent.description,
                    'category': installed.agent.category,
                    'icon': installed.agent.icon,
                    'version': installed.agent.version
                }

            # Decrypt config for display (mask sensitive values)
            if installed.config_json:
                decrypted = decrypt_dict(installed.config_json)
                # Mask sensitive values
                masked_config = {}
                for key, value in decrypted.items():
                    if any(sensitive in key.lower() for sensitive in ['key', 'secret', 'password', 'token']):
                        masked_config[key] = '***' + value[-4:] if len(value) > 4 else '***'
                    else:
                        masked_config[key] = value
                data['config'] = masked_config

            result.append(data)

        return result

    @staticmethod
    def update_agent_config(
        user_id: str,
        installed_agent_id: str,
        new_config: Dict
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Update configuration for an installed agent

        Returns:
            Tuple of (updated_agent_dict, error_message)
        """
        installed_agent = InstalledAgent.query.filter_by(
            id=installed_agent_id,
            user_id=user_id
        ).first()

        if not installed_agent:
            return None, 'Installed agent not found'

        # Validate required env vars
        if installed_agent.agent and installed_agent.agent.env_vars_required:
            missing_vars = []
            for var in installed_agent.agent.env_vars_required:
                if var not in new_config:
                    missing_vars.append(var)

            if missing_vars:
                return None, f'Missing required configuration: {", ".join(missing_vars)}'

        # Encrypt and update
        encrypted_config = encrypt_dict(new_config)
        installed_agent.config_json = encrypted_config
        installed_agent.updated_at = datetime.utcnow()
        db.session.commit()

        return installed_agent.to_dict(), None

    @staticmethod
    def toggle_agent_enabled(
        user_id: str,
        installed_agent_id: str,
        enabled: bool
    ) -> Tuple[bool, Optional[str]]:
        """
        Enable or disable an installed agent

        Returns:
            Tuple of (success, error_message)
        """
        installed_agent = InstalledAgent.query.filter_by(
            id=installed_agent_id,
            user_id=user_id
        ).first()

        if not installed_agent:
            return False, 'Installed agent not found'

        installed_agent.is_enabled = enabled
        installed_agent.updated_at = datetime.utcnow()
        db.session.commit()

        return True, None

    @staticmethod
    def get_agent_config(user_id: str, installed_agent_id: str) -> Optional[Dict]:
        """
        Get decrypted configuration for an installed agent
        Used during agent execution

        Returns:
            Decrypted config dict or None
        """
        installed_agent = InstalledAgent.query.filter_by(
            id=installed_agent_id,
            user_id=user_id
        ).first()

        if not installed_agent or not installed_agent.config_json:
            return None

        return decrypt_dict(installed_agent.config_json)


# Convenience functions
def browse_agents(*args, **kwargs):
    """Browse agents in marketplace"""
    return AgentService.browse_agents(*args, **kwargs)


def get_agent_detail(agent_id: str):
    """Get agent details"""
    return AgentService.get_agent_detail(agent_id)


def install_agent(user_id: str, agent_id: str, config: Optional[Dict] = None):
    """Install agent for user"""
    return AgentService.install_agent(user_id, agent_id, config)


def uninstall_agent(user_id: str, installed_agent_id: str):
    """Uninstall agent"""
    return AgentService.uninstall_agent(user_id, installed_agent_id)


def get_user_installed_agents(user_id: str):
    """Get user's installed agents"""
    return AgentService.get_user_installed_agents(user_id)


def update_agent_config(user_id: str, installed_agent_id: str, new_config: Dict):
    """Update agent configuration"""
    return AgentService.update_agent_config(user_id, installed_agent_id, new_config)


def toggle_agent_enabled(user_id: str, installed_agent_id: str, enabled: bool):
    """Toggle agent enabled state"""
    return AgentService.toggle_agent_enabled(user_id, installed_agent_id, enabled)


def get_agent_config(user_id: str, installed_agent_id: str):
    """Get decrypted agent configuration"""
    return AgentService.get_agent_config(user_id, installed_agent_id)
