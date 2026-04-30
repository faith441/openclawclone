"""
API Keys Model - Bring Your Own Key (BYOK) System
Securely stores user's API keys for various AI providers
"""
from datetime import datetime
from .base import db, BaseModel


class UserAPIKey(db.Model, BaseModel):
    """
    User's API keys for AI providers
    Keys are stored encrypted
    """
    __tablename__ = 'user_api_keys'

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)

    # Provider (openai, anthropic, google, groq, etc.)
    provider = db.Column(db.String(50), nullable=False, index=True)

    # Encrypted API key
    encrypted_key = db.Column(db.Text, nullable=False)

    # Key metadata
    key_name = db.Column(db.String(100))  # User-friendly name
    key_prefix = db.Column(db.String(10))  # First few chars for identification
    is_active = db.Column(db.Boolean, default=True)

    # Usage tracking
    last_used_at = db.Column(db.DateTime)
    total_requests = db.Column(db.Integer, default=0)
    total_tokens = db.Column(db.Integer, default=0)
    total_cost_usd = db.Column(db.Float, default=0.0)

    # Validation status
    is_valid = db.Column(db.Boolean, default=True)
    last_validated_at = db.Column(db.DateTime)
    validation_error = db.Column(db.Text)

    # Unique constraint per user per provider
    __table_args__ = (
        db.UniqueConstraint('user_id', 'provider', name='unique_user_provider'),
    )

    # Relationship
    user = db.relationship('User', backref=db.backref('api_keys', lazy='dynamic'))

    def to_dict(self, include_key=False):
        """Convert to dict (never include full key by default)"""
        result = {
            'id': self.id,
            'provider': self.provider,
            'key_name': self.key_name,
            'key_prefix': self.key_prefix,
            'is_active': self.is_active,
            'is_valid': self.is_valid,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'total_requests': self.total_requests,
            'total_tokens': self.total_tokens,
            'total_cost_usd': round(self.total_cost_usd, 4),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_key:
            result['encrypted_key'] = self.encrypted_key

        return result

    def update_usage(self, tokens: int, cost: float):
        """Update usage statistics"""
        self.last_used_at = datetime.utcnow()
        self.total_requests += 1
        self.total_tokens += tokens
        self.total_cost_usd += cost
        db.session.commit()

    def mark_invalid(self, error: str):
        """Mark key as invalid"""
        self.is_valid = False
        self.validation_error = error
        self.last_validated_at = datetime.utcnow()
        db.session.commit()

    def mark_valid(self):
        """Mark key as valid"""
        self.is_valid = True
        self.validation_error = None
        self.last_validated_at = datetime.utcnow()
        db.session.commit()


class UserPreferences(db.Model, BaseModel):
    """
    User preferences for AI and automation settings
    """
    __tablename__ = 'user_preferences'

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, unique=True)

    # Default AI model preference
    default_model = db.Column(db.String(50), default='gpt-4o-mini')

    # Auto-select settings
    auto_select_model = db.Column(db.Boolean, default=True)  # Auto-pick best model for task
    prefer_local_models = db.Column(db.Boolean, default=False)  # Prefer Ollama if available
    prefer_cheap_models = db.Column(db.Boolean, default=False)  # Optimize for cost

    # Execution preferences
    max_tokens_per_request = db.Column(db.Integer, default=4096)
    enable_streaming = db.Column(db.Boolean, default=True)
    auto_retry_on_failure = db.Column(db.Boolean, default=True)
    max_retries = db.Column(db.Integer, default=3)

    # Budget controls
    daily_budget_usd = db.Column(db.Float)  # Daily spending limit
    monthly_budget_usd = db.Column(db.Float)  # Monthly spending limit
    alert_at_percentage = db.Column(db.Integer, default=80)  # Alert when X% of budget used

    # Ollama settings (for local models)
    ollama_base_url = db.Column(db.String(255), default='http://localhost:11434')

    # Relationship
    user = db.relationship('User', backref=db.backref('preferences', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'default_model': self.default_model,
            'auto_select_model': self.auto_select_model,
            'prefer_local_models': self.prefer_local_models,
            'prefer_cheap_models': self.prefer_cheap_models,
            'max_tokens_per_request': self.max_tokens_per_request,
            'enable_streaming': self.enable_streaming,
            'auto_retry_on_failure': self.auto_retry_on_failure,
            'max_retries': self.max_retries,
            'daily_budget_usd': self.daily_budget_usd,
            'monthly_budget_usd': self.monthly_budget_usd,
            'alert_at_percentage': self.alert_at_percentage,
            'ollama_base_url': self.ollama_base_url
        }
