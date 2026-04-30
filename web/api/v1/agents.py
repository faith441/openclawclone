"""
Agent Marketplace API Endpoints
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask import Blueprint, request, jsonify
from middleware.auth_middleware import jwt_required, get_current_user
from services.agent_service import (
    browse_agents,
    get_agent_detail,
    install_agent,
    uninstall_agent,
    get_user_installed_agents,
    update_agent_config,
    toggle_agent_enabled,
    AgentService
)

agents_bp = Blueprint('agents', __name__)


@agents_bp.route('/browse', methods=['GET'])
def browse_agents_endpoint():
    """
    Browse agents in marketplace
    Query params: category, search, limit, offset
    """
    try:
        category = request.args.get('category')
        search_query = request.args.get('search')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))

        agents, total_count = browse_agents(
            category=category,
            search_query=search_query,
            limit=limit,
            offset=offset
        )

        return jsonify({
            'success': True,
            'agents': agents,
            'total': total_count,
            'limit': limit,
            'offset': offset
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@agents_bp.route('/categories', methods=['GET'])
def get_categories_endpoint():
    """Get all agent categories with counts"""
    try:
        categories = AgentService.get_categories()

        return jsonify({
            'success': True,
            'categories': categories
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@agents_bp.route('/<agent_id>', methods=['GET'])
def get_agent_detail_endpoint(agent_id):
    """Get detailed information about a specific agent"""
    try:
        agent = get_agent_detail(agent_id)

        if not agent:
            return jsonify({
                'success': False,
                'error': 'Agent not found'
            }), 404

        return jsonify({
            'success': True,
            'agent': agent
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@agents_bp.route('/install', methods=['POST'])
@jwt_required
def install_agent_endpoint():
    """
    Install an agent for the current user
    Body: { "agent_id": "uuid", "config": {...} }
    """
    try:
        user = get_current_user()
        data = request.get_json()

        agent_id = data.get('agent_id')
        config = data.get('config')

        if not agent_id:
            return jsonify({
                'success': False,
                'error': 'agent_id is required'
            }), 400

        installed_agent, error = install_agent(user.id, agent_id, config)

        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400

        return jsonify({
            'success': True,
            'installed_agent': installed_agent,
            'message': 'Agent installed successfully'
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@agents_bp.route('/installed', methods=['GET'])
@jwt_required
def get_installed_agents_endpoint():
    """Get all agents installed by the current user"""
    try:
        user = get_current_user()
        installed_agents = get_user_installed_agents(user.id)

        return jsonify({
            'success': True,
            'installed_agents': installed_agents,
            'count': len(installed_agents)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@agents_bp.route('/installed/<installed_agent_id>', methods=['DELETE'])
@jwt_required
def uninstall_agent_endpoint(installed_agent_id):
    """Uninstall an agent"""
    try:
        user = get_current_user()
        success, error = uninstall_agent(user.id, installed_agent_id)

        if not success:
            return jsonify({
                'success': False,
                'error': error
            }), 404

        return jsonify({
            'success': True,
            'message': 'Agent uninstalled successfully'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@agents_bp.route('/installed/<installed_agent_id>/config', methods=['PUT'])
@jwt_required
def update_agent_config_endpoint(installed_agent_id):
    """
    Update configuration for an installed agent
    Body: { "config": {...} }
    """
    try:
        user = get_current_user()
        data = request.get_json()

        new_config = data.get('config')

        if not new_config:
            return jsonify({
                'success': False,
                'error': 'config is required'
            }), 400

        updated_agent, error = update_agent_config(user.id, installed_agent_id, new_config)

        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400

        return jsonify({
            'success': True,
            'installed_agent': updated_agent,
            'message': 'Configuration updated successfully'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@agents_bp.route('/installed/<installed_agent_id>/toggle', methods=['POST'])
@jwt_required
def toggle_agent_enabled_endpoint(installed_agent_id):
    """
    Enable or disable an installed agent
    Body: { "enabled": true/false }
    """
    try:
        user = get_current_user()
        data = request.get_json()

        enabled = data.get('enabled')

        if enabled is None:
            return jsonify({
                'success': False,
                'error': 'enabled is required'
            }), 400

        success, error = toggle_agent_enabled(user.id, installed_agent_id, enabled)

        if not success:
            return jsonify({
                'success': False,
                'error': error
            }), 404

        return jsonify({
            'success': True,
            'message': f'Agent {"enabled" if enabled else "disabled"} successfully'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
