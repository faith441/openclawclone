"""
API routes for Zenthral AI Platform
"""
from flask import Blueprint

# Create API blueprint
api = Blueprint('api', __name__, url_prefix='/api')

# Import and register v1 routes
from .v1 import auth_bp, agents_bp, executions_bp, api_keys_bp, workflows_bp

api.register_blueprint(auth_bp, url_prefix='/v1/auth')
api.register_blueprint(agents_bp, url_prefix='/v1/agents')
api.register_blueprint(executions_bp, url_prefix='/v1/executions')
api.register_blueprint(api_keys_bp, url_prefix='/v1/api-keys')
api.register_blueprint(workflows_bp, url_prefix='/v1/workflows')

__all__ = ['api']
