"""
Agent catalog and installed agents models
"""
from . import db, BaseModel
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Text


class AgentCatalog(db.Model, BaseModel):
    """Agent catalog - all available agents in the marketplace"""

    __tablename__ = 'agent_catalog'

    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(Text)
    category = db.Column(db.String(100), index=True)  # finance, real-estate, ecommerce, automation
    industry = db.Column(db.String(100))
    icon = db.Column(db.String(10))  # emoji
    version = db.Column(db.String(50), default='1.0.0')

    # File paths
    file_path = db.Column(db.String(500), nullable=False)  # path to agent script
    skill_md_path = db.Column(db.String(500))  # path to SKILL.md

    # Metadata stored as JSON
    requirements_json = db.Column(db.JSON)  # parsed requirements.txt
    env_vars_required = db.Column(db.JSON)  # ['STRIPE_API_KEY', 'ANTHROPIC_API_KEY']
    config_schema = db.Column(db.JSON)  # JSON schema for configuration

    # Publishing
    is_published = db.Column(db.Boolean, default=True, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)

    # Stats
    install_count = db.Column(db.Integer, default=0, nullable=False)
    rating_avg = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0, nullable=False)

    # Relationships
    installed_agents = db.relationship('InstalledAgent', back_populates='agent', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<AgentCatalog {self.slug}>'

    def to_dict(self):
        """Convert agent to dictionary"""
        return {
            'id': self.id,
            'slug': self.slug,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'industry': self.industry,
            'icon': self.icon,
            'version': self.version,
            'file_path': self.file_path,
            'requirements': self.requirements_json,
            'env_vars_required': self.env_vars_required,
            'is_published': self.is_published,
            'is_featured': self.is_featured,
            'install_count': self.install_count,
            'rating_avg': round(self.rating_avg, 2) if self.rating_avg else 0.0,
            'rating_count': self.rating_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class InstalledAgent(db.Model, BaseModel):
    """User's installed agents"""

    __tablename__ = 'installed_agents'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'agent_id', name='unique_user_agent'),
    )

    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id', ondelete='CASCADE'), index=True)
    agent_id = db.Column(db.String(36), db.ForeignKey('agent_catalog.id', ondelete='CASCADE'), nullable=False, index=True)

    # User customization
    custom_name = db.Column(db.String(255))  # user can rename
    is_enabled = db.Column(db.Boolean, default=True, nullable=False)

    # Configuration stored as encrypted JSON
    config_json = db.Column(db.JSON)  # user-specific configuration

    # Usage stats
    last_run_at = db.Column(db.DateTime)
    run_count = db.Column(db.Integer, default=0, nullable=False)

    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    organization = db.relationship('Organization', foreign_keys=[organization_id])
    agent = db.relationship('AgentCatalog', back_populates='installed_agents')

    def __repr__(self):
        return f'<InstalledAgent {self.agent_id} for user {self.user_id}>'

    def to_dict(self):
        """Convert installed agent to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'organization_id': self.organization_id,
            'agent_id': self.agent_id,
            'agent': self.agent.to_dict() if self.agent else None,
            'custom_name': self.custom_name,
            'is_enabled': self.is_enabled,
            'config_json': self.config_json,  # Don't expose sensitive config
            'last_run_at': self.last_run_at.isoformat() if self.last_run_at else None,
            'run_count': self.run_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @property
    def display_name(self):
        """Get display name (custom or default)"""
        return self.custom_name or (self.agent.name if self.agent else 'Unknown Agent')
