"""
API v1 routes
"""
from flask import Blueprint

# Import blueprints
from .auth import auth_bp
from .agents import agents_bp
from .executions import executions_bp
from .api_keys import api_keys_bp
from .workflows import workflows_bp

__all__ = ['auth_bp', 'agents_bp', 'executions_bp', 'api_keys_bp', 'workflows_bp']
