"""
JWT utility functions for authentication
"""
import jwt
from datetime import datetime, timedelta
from flask import current_app


def encode_token(payload, secret=None, expires_in=None):
    """
    Encode JWT token

    Args:
        payload (dict): Token payload
        secret (str): Secret key (uses app config if not provided)
        expires_in (int): Expiration time in seconds

    Returns:
        str: Encoded JWT token
    """
    if secret is None:
        secret = current_app.config['JWT_SECRET']

    # Add timestamp
    payload['iat'] = datetime.utcnow()

    # Add expiration if specified
    if expires_in:
        payload['exp'] = datetime.utcnow() + timedelta(seconds=expires_in)

    return jwt.encode(payload, secret, algorithm='HS256')


def decode_token(token, secret=None):
    """
    Decode JWT token

    Args:
        token (str): JWT token
        secret (str): Secret key (uses app config if not provided)

    Returns:
        dict: Decoded payload or None if invalid

    Raises:
        jwt.ExpiredSignatureError: Token has expired
        jwt.InvalidTokenError: Token is invalid
    """
    if secret is None:
        secret = current_app.config['JWT_SECRET']

    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError('Token has expired')
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError('Invalid token')


def create_access_token(user_id, email, organization_id=None, role='member'):
    """
    Create access token for user

    Args:
        user_id (str): User ID
        email (str): User email
        organization_id (str): Organization ID (optional)
        role (str): User role in organization

    Returns:
        str: Access token
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'type': 'access'
    }

    if organization_id:
        payload['organization_id'] = organization_id
        payload['role'] = role

    expires_in = current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    return encode_token(payload, expires_in=expires_in)


def create_refresh_token(user_id):
    """
    Create refresh token for user

    Args:
        user_id (str): User ID

    Returns:
        str: Refresh token
    """
    payload = {
        'user_id': user_id,
        'type': 'refresh'
    }

    expires_in = current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
    return encode_token(payload, expires_in=expires_in)


def verify_access_token(token):
    """
    Verify access token and return payload

    Args:
        token (str): Access token

    Returns:
        dict: Token payload or None if invalid
    """
    try:
        payload = decode_token(token)
        if payload.get('type') != 'access':
            return None
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def verify_refresh_token(token):
    """
    Verify refresh token and return payload

    Args:
        token (str): Refresh token

    Returns:
        dict: Token payload or None if invalid
    """
    try:
        payload = decode_token(token)
        if payload.get('type') != 'refresh':
            return None
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
