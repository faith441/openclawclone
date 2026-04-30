"""
Authentication middleware for JWT token verification
"""
from functools import wraps
from flask import request, jsonify, g
from models import User
from utils.jwt_utils import verify_access_token
import jwt


def get_current_user():
    """
    Get current authenticated user from request context

    Returns:
        User: Current user or None
    """
    return getattr(g, 'current_user', None)


def extract_token_from_header():
    """
    Extract JWT token from Authorization header

    Returns:
        str: Token or None
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None

    return parts[1]


def jwt_required(f):
    """
    Decorator to protect routes with JWT authentication

    Usage:
        @app.route('/protected')
        @jwt_required
        def protected_route():
            user = get_current_user()
            return jsonify({'user_id': user.id})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = extract_token_from_header()

        if not token:
            return jsonify({
                'success': False,
                'error': 'Authentication required. Please provide a valid access token.'
            }), 401

        try:
            # Verify token
            payload = verify_access_token(token)
            if not payload:
                return jsonify({
                    'success': False,
                    'error': 'Invalid or expired token'
                }), 401

            # Get user from database
            user_id = payload.get('user_id')
            user = User.get(user_id)

            if not user or user.status != 'active':
                return jsonify({
                    'success': False,
                    'error': 'User not found or inactive'
                }), 401

            # Store user in request context
            g.current_user = user
            g.token_payload = payload

            return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'error': 'Token has expired. Please refresh your token.'
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'error': 'Invalid token'
            }), 401

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Authentication failed: {str(e)}'
            }), 500

    return decorated_function


def optional_auth(f):
    """
    Decorator for routes that optionally accept authentication
    User will be available if token is provided, but route works without it

    Usage:
        @app.route('/public')
        @optional_auth
        def public_route():
            user = get_current_user()
            if user:
                return jsonify({'message': f'Hello {user.email}'})
            return jsonify({'message': 'Hello guest'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = extract_token_from_header()

        if token:
            try:
                payload = verify_access_token(token)
                if payload:
                    user_id = payload.get('user_id')
                    user = User.get(user_id)
                    if user and user.status == 'active':
                        g.current_user = user
                        g.token_payload = payload
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                pass  # Ignore invalid tokens for optional auth

        return f(*args, **kwargs)

    return decorated_function


def role_required(*roles):
    """
    Decorator to require specific roles

    Usage:
        @app.route('/admin')
        @jwt_required
        @role_required('owner', 'admin')
        def admin_route():
            return jsonify({'message': 'Admin access'})
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            payload = getattr(g, 'token_payload', {})
            user_role = payload.get('role', 'member')

            if user_role not in roles:
                return jsonify({
                    'success': False,
                    'error': f'Insufficient permissions. Required roles: {", ".join(roles)}'
                }), 403

            return f(*args, **kwargs)

        return decorated_function
    return decorator
