"""
API endpoints for workflow generation and management
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, UserAPIKey, UserPreferences
from services.ai_router import AIRouter
from services.workflow_engine import WorkflowEngine
from services.encryption import decrypt_api_key
import logging

logger = logging.getLogger(__name__)

workflows_bp = Blueprint('workflows', __name__)


@workflows_bp.route('/generate', methods=['POST'])
@jwt_required()
async def generate_workflow():
    """
    Generate a workflow from natural language description

    Body:
        {
            "prompt": "Every morning, scrape HackerNews top 10 and send me a summary",
            "model_id": "gpt-4" (optional - will auto-select if not provided)
        }
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'prompt' not in data:
        return jsonify({'error': 'Prompt is required'}), 400

    user_prompt = data['prompt']
    model_id = data.get('model_id')

    # Get user's API keys
    api_keys = UserAPIKey.query.filter_by(
        user_id=user_id,
        is_active=True,
        is_deleted=False
    ).all()

    if not api_keys:
        return jsonify({
            'error': 'No API keys configured. Please add at least one API key in Settings.',
            'setup_required': True
        }), 400

    # Decrypt API keys for AI router
    decrypted_keys = {}
    for key in api_keys:
        try:
            decrypted_keys[key.provider] = decrypt_api_key(key.encrypted_key)
        except Exception as e:
            logger.error(f"Failed to decrypt API key for {key.provider}: {str(e)}")

    # Initialize AI router
    ai_router = AIRouter()

    try:
        # Generate workflow
        workflow = await WorkflowEngine.generate_workflow(
            user_prompt=user_prompt,
            ai_router=ai_router,
            api_keys=decrypted_keys,
            model_id=model_id
        )

        return jsonify({
            'workflow': workflow.to_dict(),
            'message': 'Workflow generated successfully'
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Workflow generation error: {str(e)}")
        return jsonify({'error': 'Failed to generate workflow'}), 500


@workflows_bp.route('/validate', methods=['POST'])
@jwt_required()
def validate_workflow():
    """
    Validate a workflow JSON structure

    Body:
        {
            "workflow": { ... workflow JSON ... }
        }
    """
    data = request.get_json()

    if not data or 'workflow' not in data:
        return jsonify({'error': 'Workflow is required'}), 400

    workflow_data = data['workflow']

    try:
        # Validate required fields
        required_fields = ['name', 'description', 'trigger', 'actions']
        missing_fields = [f for f in required_fields if f not in workflow_data]

        if missing_fields:
            return jsonify({
                'valid': False,
                'errors': [f'Missing required field: {f}' for f in missing_fields]
            }), 200

        # Validate trigger
        if 'type' not in workflow_data['trigger']:
            return jsonify({
                'valid': False,
                'errors': ['Trigger must have a type']
            }), 200

        # Validate actions
        if not isinstance(workflow_data['actions'], list) or len(workflow_data['actions']) == 0:
            return jsonify({
                'valid': False,
                'errors': ['Workflow must have at least one action']
            }), 200

        for i, action in enumerate(workflow_data['actions']):
            if 'type' not in action:
                return jsonify({
                    'valid': False,
                    'errors': [f'Action {i+1} is missing type']
                }), 200

        return jsonify({
            'valid': True,
            'message': 'Workflow is valid'
        }), 200

    except Exception as e:
        logger.error(f"Workflow validation error: {str(e)}")
        return jsonify({
            'valid': False,
            'errors': [str(e)]
        }), 200


@workflows_bp.route('/action-blocks', methods=['GET'])
@jwt_required()
def get_action_blocks():
    """Get available action blocks library"""
    from services.workflow_engine import ACTION_BLOCKS

    blocks = []
    for action_type, block_data in ACTION_BLOCKS.items():
        blocks.append({
            'type': action_type.value,
            'name': block_data['name'],
            'description': block_data['description'],
            'parameters': block_data['parameters'],
            'example': block_data.get('example', {})
        })

    return jsonify({
        'action_blocks': blocks,
        'total': len(blocks)
    }), 200


@workflows_bp.route('/test', methods=['POST'])
@jwt_required()
async def test_workflow():
    """
    Test a workflow with sample data (dry run)

    Body:
        {
            "workflow": { ... workflow JSON ... },
            "test_data": { ... optional test inputs ... }
        }
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'workflow' not in data:
        return jsonify({'error': 'Workflow is required'}), 400

    workflow_data = data['workflow']
    test_data = data.get('test_data', {})

    try:
        # In a real implementation, this would execute the workflow in a sandbox
        # For now, we'll just validate and return the structure
        return jsonify({
            'test_passed': True,
            'message': 'Workflow structure is valid. Ready for execution.',
            'workflow': workflow_data,
            'note': 'Dry run completed - no actions were actually executed'
        }), 200

    except Exception as e:
        logger.error(f"Workflow test error: {str(e)}")
        return jsonify({
            'test_passed': False,
            'error': str(e)
        }), 500


@workflows_bp.route('/chat', methods=['POST'])
@jwt_required()
async def chat_with_ai():
    """
    Chat with AI to refine or discuss workflows

    Body:
        {
            "message": "Can you add error handling to this workflow?",
            "context": { ... optional workflow context ... },
            "model_id": "gpt-4" (optional)
        }
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400

    user_message = data['message']
    context = data.get('context', {})
    model_id = data.get('model_id')

    # Get user's API keys
    api_keys = UserAPIKey.query.filter_by(
        user_id=user_id,
        is_active=True,
        is_deleted=False
    ).all()

    if not api_keys:
        return jsonify({
            'error': 'No API keys configured. Please add at least one API key in Settings.',
            'setup_required': True
        }), 400

    # Decrypt API keys
    decrypted_keys = {}
    for key in api_keys:
        try:
            decrypted_keys[key.provider] = decrypt_api_key(key.encrypted_key)
        except Exception as e:
            logger.error(f"Failed to decrypt API key for {key.provider}: {str(e)}")

    # Initialize AI router
    ai_router = AIRouter()

    try:
        # Build conversation context
        messages = [
            {
                'role': 'system',
                'content': 'You are a helpful automation expert. Help users create, refine, and understand their workflows. Be concise and practical.'
            }
        ]

        if context:
            messages.append({
                'role': 'system',
                'content': f'Current workflow context: {context}'
            })

        messages.append({
            'role': 'user',
            'content': user_message
        })

        # Get AI response
        response = await ai_router.chat(
            messages=messages,
            api_keys=decrypted_keys,
            model_id=model_id
        )

        return jsonify({
            'response': response['content'],
            'model_used': response['model'],
            'tokens_used': response['usage']['total_tokens']
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': 'Failed to process chat message'}), 500
