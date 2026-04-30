"""
API endpoints for managing user API keys (BYOK - Bring Your Own Key)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, UserAPIKey, UserPreferences
from services.encryption import encrypt_api_key, decrypt_api_key
import logging

logger = logging.getLogger(__name__)

api_keys_bp = Blueprint('api_keys', __name__)


@api_keys_bp.route('/providers', methods=['GET'])
@jwt_required()
def get_providers():
    """Get list of supported AI providers"""
    providers = [
        {
            'id': 'openai',
            'name': 'OpenAI',
            'description': 'GPT-4, GPT-3.5, and other OpenAI models',
            'models': ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'],
            'signup_url': 'https://platform.openai.com/signup'
        },
        {
            'id': 'anthropic',
            'name': 'Anthropic',
            'description': 'Claude Opus, Sonnet, and Haiku models',
            'models': ['claude-opus-4-5', 'claude-sonnet-4-5', 'claude-haiku-4'],
            'signup_url': 'https://console.anthropic.com/'
        },
        {
            'id': 'google',
            'name': 'Google AI',
            'description': 'Gemini models',
            'models': ['gemini-2.0-flash', 'gemini-1.5-pro'],
            'signup_url': 'https://ai.google.dev/'
        },
        {
            'id': 'groq',
            'name': 'Groq',
            'description': 'Fast inference for Llama and Mixtral models',
            'models': ['llama-3.3-70b', 'mixtral-8x7b'],
            'signup_url': 'https://console.groq.com/'
        },
        {
            'id': 'ollama',
            'name': 'Ollama',
            'description': 'Local models (no API key required)',
            'models': ['llama3.3', 'mistral', 'codellama'],
            'signup_url': 'https://ollama.ai/download',
            'local': True
        }
    ]

    return jsonify({'providers': providers}), 200


@api_keys_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_api_keys():
    """Get all API keys for the current user (returns masked keys)"""
    user_id = get_jwt_identity()

    api_keys = UserAPIKey.query.filter_by(user_id=user_id, is_deleted=False).all()

    keys_data = []
    for key in api_keys:
        # Decrypt and mask the key for display
        try:
            decrypted = decrypt_api_key(key.encrypted_key)
            masked = f"{decrypted[:8]}...{decrypted[-4:]}" if len(decrypted) > 12 else "***"
        except:
            masked = "***"

        keys_data.append({
            'id': key.id,
            'provider': key.provider,
            'masked_key': masked,
            'is_active': key.is_active,
            'created_at': key.created_at.isoformat(),
            'last_used': key.last_used.isoformat() if key.last_used else None
        })

    return jsonify({'api_keys': keys_data}), 200


@api_keys_bp.route('/', methods=['POST'])
@jwt_required()
def add_api_key():
    """Add a new API key for a provider"""
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'provider' not in data or 'api_key' not in data:
        return jsonify({'error': 'Provider and API key are required'}), 400

    provider = data['provider'].lower()
    api_key_value = data['api_key'].strip()

    # Validate provider
    valid_providers = ['openai', 'anthropic', 'google', 'groq', 'ollama']
    if provider not in valid_providers:
        return jsonify({'error': f'Invalid provider. Must be one of: {", ".join(valid_providers)}'}), 400

    # Check if user already has a key for this provider
    existing_key = UserAPIKey.query.filter_by(
        user_id=user_id,
        provider=provider,
        is_deleted=False
    ).first()

    if existing_key:
        # Update existing key
        existing_key.encrypted_key = encrypt_api_key(api_key_value)
        existing_key.is_active = True
        db.session.commit()

        return jsonify({
            'message': f'API key for {provider} updated successfully',
            'key_id': existing_key.id
        }), 200
    else:
        # Create new key
        new_key = UserAPIKey(
            user_id=user_id,
            provider=provider,
            encrypted_key=encrypt_api_key(api_key_value),
            is_active=True
        )
        db.session.add(new_key)
        db.session.commit()

        return jsonify({
            'message': f'API key for {provider} added successfully',
            'key_id': new_key.id
        }), 201


@api_keys_bp.route('/<key_id>', methods=['DELETE'])
@jwt_required()
def delete_api_key(key_id):
    """Delete an API key"""
    user_id = get_jwt_identity()

    api_key = UserAPIKey.query.filter_by(id=key_id, user_id=user_id).first()
    if not api_key:
        return jsonify({'error': 'API key not found'}), 404

    api_key.soft_delete()
    db.session.commit()

    return jsonify({'message': 'API key deleted successfully'}), 200


@api_keys_bp.route('/<key_id>/toggle', methods=['POST'])
@jwt_required()
def toggle_api_key(key_id):
    """Toggle an API key active/inactive"""
    user_id = get_jwt_identity()

    api_key = UserAPIKey.query.filter_by(id=key_id, user_id=user_id, is_deleted=False).first()
    if not api_key:
        return jsonify({'error': 'API key not found'}), 404

    api_key.is_active = not api_key.is_active
    db.session.commit()

    return jsonify({
        'message': f'API key {"activated" if api_key.is_active else "deactivated"}',
        'is_active': api_key.is_active
    }), 200


@api_keys_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_preferences():
    """Get user AI preferences"""
    user_id = get_jwt_identity()

    prefs = UserPreferences.query.filter_by(user_id=user_id).first()
    if not prefs:
        # Create default preferences
        prefs = UserPreferences(user_id=user_id)
        db.session.add(prefs)
        db.session.commit()

    return jsonify({
        'preferences': {
            'default_provider': prefs.default_provider,
            'default_model': prefs.default_model,
            'temperature': prefs.temperature,
            'max_tokens': prefs.max_tokens,
            'budget_limit': prefs.budget_limit,
            'budget_period': prefs.budget_period,
            'auto_select_model': prefs.auto_select_model
        }
    }), 200


@api_keys_bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_preferences():
    """Update user AI preferences"""
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    prefs = UserPreferences.query.filter_by(user_id=user_id).first()
    if not prefs:
        prefs = UserPreferences(user_id=user_id)
        db.session.add(prefs)

    # Update allowed fields
    if 'default_provider' in data:
        prefs.default_provider = data['default_provider']
    if 'default_model' in data:
        prefs.default_model = data['default_model']
    if 'temperature' in data:
        prefs.temperature = float(data['temperature'])
    if 'max_tokens' in data:
        prefs.max_tokens = int(data['max_tokens'])
    if 'budget_limit' in data:
        prefs.budget_limit = float(data['budget_limit']) if data['budget_limit'] else None
    if 'budget_period' in data:
        prefs.budget_period = data['budget_period']
    if 'auto_select_model' in data:
        prefs.auto_select_model = bool(data['auto_select_model'])

    db.session.commit()

    return jsonify({'message': 'Preferences updated successfully'}), 200
