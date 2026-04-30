"""
Authentication API endpoints
"""
from flask import Blueprint, request, jsonify
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from services.auth_service import AuthService
from models import User

# No url_prefix here - it's set when registered to parent blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register new user

    POST /api/v1/auth/register
    {
        "email": "user@example.com",
        "password": "SecurePass123!",
        "full_name": "John Doe"
    }

    Returns:
    {
        "success": true,
        "message": "Registration successful. Please check your email to verify your account.",
        "user": {...}
    }
    """
    try:
        data = request.get_json()

        # Validate input
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name', '')

        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400

        # Register user
        user, error = AuthService.register_user(email, password, full_name)

        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400

        return jsonify({
            'success': True,
            'message': 'Registration successful. Please check your email to verify your account.',
            'user': user.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Registration failed: {str(e)}'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user

    POST /api/v1/auth/login
    {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }

    Returns:
    {
        "success": true,
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "user": {...}
    }
    """
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400

        # Login user
        result, error = AuthService.login_user(email, password)

        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 401

        return jsonify({
            'success': True,
            **result
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Login failed: {str(e)}'
        }), 500


@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    """
    Verify user email with token

    POST /api/v1/auth/verify-email
    {
        "token": "abc123..."
    }

    Returns:
    {
        "success": true,
        "message": "Email verified successfully",
        "user": {...}
    }
    """
    try:
        data = request.get_json()
        token = data.get('token')

        if not token:
            return jsonify({
                'success': False,
                'error': 'Verification token is required'
            }), 400

        user, error = AuthService.verify_email(token)

        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400

        return jsonify({
            'success': True,
            'message': 'Email verified successfully',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Verification failed: {str(e)}'
        }), 500


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Request password reset

    POST /api/v1/auth/forgot-password
    {
        "email": "user@example.com"
    }

    Returns:
    {
        "success": true,
        "message": "If an account exists with this email, you will receive a password reset link."
    }
    """
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({
                'success': False,
                'error': 'Email is required'
            }), 400

        # Request password reset
        AuthService.request_password_reset(email)

        # Always return success to prevent email enumeration
        return jsonify({
            'success': True,
            'message': 'If an account exists with this email, you will receive a password reset link.'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Request failed: {str(e)}'
        }), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Reset password with token

    POST /api/v1/auth/reset-password
    {
        "token": "abc123...",
        "password": "NewSecurePass123!"
    }

    Returns:
    {
        "success": true,
        "message": "Password reset successfully"
    }
    """
    try:
        data = request.get_json()
        token = data.get('token')
        password = data.get('password')

        if not token or not password:
            return jsonify({
                'success': False,
                'error': 'Token and new password are required'
            }), 400

        success, error = AuthService.reset_password(token, password)

        if not success:
            return jsonify({
                'success': False,
                'error': error
            }), 400

        return jsonify({
            'success': True,
            'message': 'Password reset successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Password reset failed: {str(e)}'
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """
    Refresh access token

    POST /api/v1/auth/refresh
    {
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }

    Returns:
    {
        "success": true,
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
    """
    try:
        data = request.get_json()
        refresh_token = data.get('refresh_token')

        if not refresh_token:
            return jsonify({
                'success': False,
                'error': 'Refresh token is required'
            }), 400

        access_token, error = AuthService.refresh_access_token(refresh_token)

        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 401

        return jsonify({
            'success': True,
            'access_token': access_token
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Token refresh failed: {str(e)}'
        }), 500


@auth_bp.route('/me', methods=['GET'])
def get_current_user_endpoint():
    """
    Get current user info (requires authentication)

    GET /api/v1/auth/me
    Headers: Authorization: Bearer <access_token>

    Returns:
    {
        "success": true,
        "user": {...}
    }
    """
    try:
        # Extract and verify token manually
        from utils.jwt_utils import verify_access_token

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Missing or invalid authorization header'
            }), 401

        token = auth_header.split(' ')[1]
        payload = verify_access_token(token)

        if not payload:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token'
            }), 401

        # Get user from database
        user_id = payload.get('user_id')
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 401

        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get user: {str(e)}'
        }), 500
