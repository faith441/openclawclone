"""
Authentication service - handles user registration, login, password management
"""
import bcrypt
import secrets
from datetime import datetime, timedelta
from flask import current_app
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import db, User, Organization
from utils.jwt_utils import create_access_token, create_refresh_token
from utils.email import send_verification_email, send_password_reset_email, send_welcome_email


class AuthService:
    """Authentication service"""

    @staticmethod
    def hash_password(password):
        """
        Hash password using bcrypt

        Args:
            password (str): Plain text password

        Returns:
            str: Hashed password
        """
        rounds = current_app.config['BCRYPT_LOG_ROUNDS']
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password, password_hash):
        """
        Verify password against hash

        Args:
            password (str): Plain text password
            password_hash (str): Hashed password

        Returns:
            bool: True if password matches
        """
        password_bytes = password.encode('utf-8')
        password_hash_bytes = password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, password_hash_bytes)

    @staticmethod
    def generate_token():
        """Generate random token for verification/reset"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def validate_password(password):
        """
        Validate password strength

        Args:
            password (str): Password to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        min_length = current_app.config['PASSWORD_MIN_LENGTH']

        if len(password) < min_length:
            return False, f'Password must be at least {min_length} characters long'

        # Check for at least one uppercase, one lowercase, one digit
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)

        if not (has_upper and has_lower and has_digit):
            return False, 'Password must contain uppercase, lowercase, and a number'

        return True, None

    @classmethod
    def register_user(cls, email, password, full_name):
        """
        Register new user

        Args:
            email (str): User email
            password (str): Plain text password
            full_name (str): User full name

        Returns:
            tuple: (user, error_message)
        """
        # Validate email
        email = email.lower().strip()
        if not email or '@' not in email:
            return None, 'Invalid email address'

        # Check if user exists
        if User.get_by(email=email):
            return None, 'Email already registered'

        # Validate password
        is_valid, error = cls.validate_password(password)
        if not is_valid:
            return None, error

        # Hash password
        password_hash = cls.hash_password(password)

        # Generate verification token
        verification_token = cls.generate_token()

        # Create user (auto-verify for development)
        user = User.create(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            email_verification_token=verification_token,
            email_verified=True  # Auto-verify for development
        )

        # Create default organization for user
        org_name = f"{full_name}'s Workspace" if full_name else f"{email.split('@')[0]}'s Workspace"
        Organization.create_with_owner(
            name=org_name,
            owner_id=user.id,
            plan_tier='free',
            billing_email=email
        )

        # Send verification email
        send_verification_email(email, full_name or 'there', verification_token)

        return user, None

    @classmethod
    def login_user(cls, email, password):
        """
        Login user

        Args:
            email (str): User email
            password (str): Plain text password

        Returns:
            tuple: (tokens_dict, error_message)
        """
        email = email.lower().strip()

        # Get user
        user = User.get_by(email=email)
        if not user:
            return None, 'Invalid email or password'

        # Verify password
        if not cls.verify_password(password, user.password_hash):
            return None, 'Invalid email or password'

        # Check if email verified (disabled for development)
        # if not user.email_verified:
        #     return None, 'Please verify your email address before logging in'

        # Check if account is active
        if user.status != 'active':
            return None, f'Account is {user.status}'

        # Update last login
        user.update(last_login_at=datetime.utcnow())

        # Get default organization
        default_org = user.default_organization
        org_id = default_org.id if default_org else None
        role = 'owner' if default_org and default_org.owner_id == user.id else 'member'

        # Generate tokens
        access_token = create_access_token(
            user_id=user.id,
            email=user.email,
            organization_id=org_id,
            role=role
        )
        refresh_token = create_refresh_token(user_id=user.id)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }, None

    @classmethod
    def verify_email(cls, token):
        """
        Verify user email with token

        Args:
            token (str): Verification token

        Returns:
            tuple: (user, error_message)
        """
        user = User.get_by(email_verification_token=token)
        if not user:
            return None, 'Invalid or expired verification token'

        if user.email_verified:
            return user, 'Email already verified'

        # Mark as verified
        user.update(
            email_verified=True,
            email_verification_token=None
        )

        # Send welcome email
        send_welcome_email(user.email, user.full_name or 'there')

        return user, None

    @classmethod
    def request_password_reset(cls, email):
        """
        Request password reset

        Args:
            email (str): User email

        Returns:
            tuple: (success, error_message)
        """
        email = email.lower().strip()
        user = User.get_by(email=email)

        # Always return success to prevent email enumeration
        if not user:
            return True, None

        # Generate reset token
        reset_token = cls.generate_token()
        expires_at = datetime.utcnow() + timedelta(hours=1)

        # Save token
        user.update(
            password_reset_token=reset_token,
            password_reset_expires_at=expires_at
        )

        # Send reset email
        send_password_reset_email(user.email, user.full_name or 'there', reset_token)

        return True, None

    @classmethod
    def reset_password(cls, token, new_password):
        """
        Reset password with token

        Args:
            token (str): Reset token
            new_password (str): New password

        Returns:
            tuple: (success, error_message)
        """
        user = User.get_by(password_reset_token=token)
        if not user:
            return False, 'Invalid or expired reset token'

        # Check if token expired
        if user.password_reset_expires_at < datetime.utcnow():
            return False, 'Reset token has expired'

        # Validate new password
        is_valid, error = cls.validate_password(new_password)
        if not is_valid:
            return False, error

        # Hash new password
        password_hash = cls.hash_password(new_password)

        # Update password and clear reset token
        user.update(
            password_hash=password_hash,
            password_reset_token=None,
            password_reset_expires_at=None
        )

        return True, None

    @classmethod
    def refresh_access_token(cls, refresh_token_str):
        """
        Generate new access token from refresh token

        Args:
            refresh_token_str (str): Refresh token

        Returns:
            tuple: (access_token, error_message)
        """
        from utils.jwt_utils import verify_refresh_token

        payload = verify_refresh_token(refresh_token_str)
        if not payload:
            return None, 'Invalid or expired refresh token'

        user_id = payload.get('user_id')
        user = User.get(user_id)
        if not user or user.status != 'active':
            return None, 'User not found or inactive'

        # Get default organization
        default_org = user.default_organization
        org_id = default_org.id if default_org else None
        role = 'owner' if default_org and default_org.owner_id == user.id else 'member'

        # Generate new access token
        access_token = create_access_token(
            user_id=user.id,
            email=user.email,
            organization_id=org_id,
            role=role
        )

        return access_token, None
