"""
User, Organization, and OrganizationMember models
"""
from . import db, BaseModel
from datetime import datetime
from slugify import slugify


class User(db.Model, BaseModel):
    """User model for authentication and profile"""

    __tablename__ = 'users'

    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255))
    avatar_url = db.Column(db.String(500))

    # Email verification
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    email_verification_token = db.Column(db.String(100))

    # Password reset
    password_reset_token = db.Column(db.String(100))
    password_reset_expires_at = db.Column(db.DateTime)

    # Onboarding
    onboarding_completed = db.Column(db.Boolean, default=False, nullable=False)

    # Activity tracking
    last_login_at = db.Column(db.DateTime)

    # Status
    status = db.Column(db.String(20), default='active', nullable=False)  # active, suspended, deleted

    # Relationships
    owned_organizations = db.relationship('Organization', back_populates='owner', foreign_keys='Organization.owner_id')
    organization_memberships = db.relationship('OrganizationMember', back_populates='user', foreign_keys='OrganizationMember.user_id', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'avatar_url': self.avatar_url,
            'email_verified': self.email_verified,
            'onboarding_completed': self.onboarding_completed,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

        if include_sensitive:
            data['password_hash'] = self.password_hash

        return data

    @property
    def default_organization(self):
        """Get user's default organization (first owned or first membership)"""
        if self.owned_organizations:
            return self.owned_organizations[0]
        if self.organization_memberships:
            return self.organization_memberships[0].organization
        return None

    @property
    def organizations(self):
        """Get all organizations user belongs to"""
        orgs = []
        for membership in self.organization_memberships:
            orgs.append(membership.organization)
        return orgs


class Organization(db.Model, BaseModel):
    """Organization/workspace model for multi-tenancy"""

    __tablename__ = 'organizations'

    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Subscription
    plan_tier = db.Column(db.String(50), default='free', nullable=False)  # free, pro, enterprise
    billing_email = db.Column(db.String(255))

    # Stripe references (for Phase 4)
    stripe_customer_id = db.Column(db.String(255), unique=True)

    # Relationships
    owner = db.relationship('User', back_populates='owned_organizations', foreign_keys=[owner_id])
    members = db.relationship('OrganizationMember', back_populates='organization', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Organization {self.name}>'

    def to_dict(self):
        """Convert organization to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'owner_id': self.owner_id,
            'plan_tier': self.plan_tier,
            'billing_email': self.billing_email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @staticmethod
    def generate_slug(name):
        """Generate unique slug from organization name"""
        base_slug = slugify(name)
        slug = base_slug
        counter = 1

        while Organization.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    @classmethod
    def create_with_owner(cls, name, owner_id, **kwargs):
        """Create organization and add owner as admin member"""
        slug = cls.generate_slug(name)
        org = cls.create(
            name=name,
            slug=slug,
            owner_id=owner_id,
            **kwargs
        )

        # Add owner as admin member
        OrganizationMember.create(
            organization_id=org.id,
            user_id=owner_id,
            role='owner'
        )

        return org


class OrganizationMember(db.Model, BaseModel):
    """Organization membership model"""

    __tablename__ = 'organization_members'
    __table_args__ = (
        db.UniqueConstraint('organization_id', 'user_id', name='unique_org_user'),
    )

    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    # Role-based access control
    role = db.Column(db.String(50), default='member', nullable=False)  # owner, admin, member, viewer

    # Invitation tracking
    invited_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    invited_at = db.Column(db.DateTime)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    organization = db.relationship('Organization', back_populates='members')
    user = db.relationship('User', back_populates='organization_memberships', foreign_keys=[user_id])
    inviter = db.relationship('User', foreign_keys=[invited_by])

    def __repr__(self):
        return f'<OrganizationMember {self.user_id} in {self.organization_id} as {self.role}>'

    def to_dict(self):
        """Convert membership to dictionary"""
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'user_id': self.user_id,
            'role': self.role,
            'invited_by': self.invited_by,
            'invited_at': self.invited_at.isoformat() if self.invited_at else None,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @property
    def can_admin(self):
        """Check if member has admin privileges"""
        return self.role in ['owner', 'admin']

    @property
    def can_write(self):
        """Check if member can write (execute agents, etc.)"""
        return self.role in ['owner', 'admin', 'member']

    @property
    def can_read(self):
        """Check if member can read"""
        return self.role in ['owner', 'admin', 'member', 'viewer']
