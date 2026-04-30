"""
Base Model for database models
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()


def generate_uuid():
    """Generate UUID for primary keys"""
    return str(uuid.uuid4())


class BaseModel:
    """Base model with common fields"""

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        """Convert model to dictionary"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result

    def save(self):
        """Save model to database"""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Delete model from database"""
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        """Update model fields"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self

    @classmethod
    def get(cls, id):
        """Get model by ID"""
        return cls.query.get(id)

    @classmethod
    def get_by(cls, **kwargs):
        """Get model by attributes"""
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def all(cls):
        """Get all models"""
        return cls.query.all()

    @classmethod
    def create(cls, **kwargs):
        """Create new model"""
        instance = cls(**kwargs)
        return instance.save()
