"""
Execution API Endpoints
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask import Blueprint, request, jsonify
from middleware.auth_middleware import jwt_required, get_current_user
from services.execution_service import (
    run_agent,
    get_execution,
    get_user_executions,
    get_usage_stats
)

executions_bp = Blueprint('executions', __name__)


@executions_bp.route('/run', methods=['POST'])
@jwt_required
def run_agent_endpoint():
    """
    Run an installed agent

    POST /api/v1/executions/run
    Body: {
        "installed_agent_id": "uuid",
        "input": {...},
        "model": "gpt-4" (optional)
    }
    """
    try:
        user = get_current_user()
        data = request.get_json()

        installed_agent_id = data.get('installed_agent_id')
        input_data = data.get('input', {})
        model_name = data.get('model', 'default')

        if not installed_agent_id:
            return jsonify({
                'success': False,
                'error': 'installed_agent_id is required'
            }), 400

        execution, error = run_agent(
            user.id,
            installed_agent_id,
            input_data,
            model_name
        )

        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400

        return jsonify({
            'success': True,
            'execution': execution,
            'message': 'Agent execution started'
        }), 202

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@executions_bp.route('/<execution_id>', methods=['GET'])
@jwt_required
def get_execution_endpoint(execution_id):
    """Get execution details and status"""
    try:
        user = get_current_user()
        execution = get_execution(user.id, execution_id)

        if not execution:
            return jsonify({
                'success': False,
                'error': 'Execution not found'
            }), 404

        return jsonify({
            'success': True,
            'execution': execution
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@executions_bp.route('/history', methods=['GET'])
@jwt_required
def get_history_endpoint():
    """
    Get execution history

    GET /api/v1/executions/history?limit=50&offset=0&status=completed
    """
    try:
        user = get_current_user()

        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        status = request.args.get('status')

        executions, total = get_user_executions(
            user.id,
            limit=limit,
            offset=offset,
            status=status
        )

        return jsonify({
            'success': True,
            'executions': executions,
            'total': total,
            'limit': limit,
            'offset': offset
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@executions_bp.route('/stats', methods=['GET'])
@jwt_required
def get_stats_endpoint():
    """
    Get usage statistics

    GET /api/v1/executions/stats?days=30
    """
    try:
        user = get_current_user()
        days = int(request.args.get('days', 30))

        stats = get_usage_stats(user.id, days)

        return jsonify({
            'success': True,
            'stats': stats
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
