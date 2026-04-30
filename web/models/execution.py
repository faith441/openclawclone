"""
Execution History Model
Tracks all agent executions with inputs, outputs, and costs
"""
from datetime import datetime
from .base import db, BaseModel


class Execution(db.Model, BaseModel):
    """
    Tracks agent execution history
    """
    __tablename__ = 'executions'

    # Foreign keys
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    installed_agent_id = db.Column(db.String(36), db.ForeignKey('installed_agents.id'), nullable=False, index=True)

    # Execution details
    status = db.Column(db.String(20), default='pending', index=True)  # pending, running, completed, failed
    input_data = db.Column(db.JSON)  # User input parameters
    output_data = db.Column(db.JSON)  # Agent output/result
    error_message = db.Column(db.Text)  # Error if failed

    # Timing
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    duration_seconds = db.Column(db.Float)  # Execution duration

    # Token usage and cost tracking
    input_tokens = db.Column(db.Integer, default=0)
    output_tokens = db.Column(db.Integer, default=0)
    total_tokens = db.Column(db.Integer, default=0)
    cost_usd = db.Column(db.Float, default=0.0)

    # Model used
    model_name = db.Column(db.String(50))  # e.g., 'gpt-4', 'claude-3'

    # Relationships
    user = db.relationship('User', backref=db.backref('executions', lazy='dynamic'))
    installed_agent = db.relationship('InstalledAgent', backref=db.backref('executions', lazy='dynamic'))

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'installed_agent_id': self.installed_agent_id,
            'status': self.status,
            'input_data': self.input_data,
            'output_data': self.output_data,
            'error_message': self.error_message,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration_seconds': self.duration_seconds,
            'input_tokens': self.input_tokens,
            'output_tokens': self.output_tokens,
            'total_tokens': self.total_tokens,
            'cost_usd': self.cost_usd,
            'model_name': self.model_name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def start(self):
        """Mark execution as started"""
        self.status = 'running'
        self.started_at = datetime.utcnow()
        db.session.commit()

    def complete(self, output_data, tokens=None, cost=None):
        """Mark execution as completed"""
        self.status = 'completed'
        self.output_data = output_data
        self.completed_at = datetime.utcnow()

        if self.started_at:
            self.duration_seconds = (self.completed_at - self.started_at).total_seconds()

        if tokens:
            self.input_tokens = tokens.get('input', 0)
            self.output_tokens = tokens.get('output', 0)
            self.total_tokens = self.input_tokens + self.output_tokens

        if cost:
            self.cost_usd = cost

        db.session.commit()

    def fail(self, error_message):
        """Mark execution as failed"""
        self.status = 'failed'
        self.error_message = error_message
        self.completed_at = datetime.utcnow()

        if self.started_at:
            self.duration_seconds = (self.completed_at - self.started_at).total_seconds()

        db.session.commit()


class UsageSummary(db.Model, BaseModel):
    """
    Daily usage summary per user
    """
    __tablename__ = 'usage_summaries'

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)

    # Counts
    total_executions = db.Column(db.Integer, default=0)
    successful_executions = db.Column(db.Integer, default=0)
    failed_executions = db.Column(db.Integer, default=0)

    # Tokens
    total_input_tokens = db.Column(db.Integer, default=0)
    total_output_tokens = db.Column(db.Integer, default=0)
    total_tokens = db.Column(db.Integer, default=0)

    # Cost
    total_cost_usd = db.Column(db.Float, default=0.0)

    # Unique constraint on user + date
    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='unique_user_date'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,
            'total_executions': self.total_executions,
            'successful_executions': self.successful_executions,
            'failed_executions': self.failed_executions,
            'total_input_tokens': self.total_input_tokens,
            'total_output_tokens': self.total_output_tokens,
            'total_tokens': self.total_tokens,
            'total_cost_usd': self.total_cost_usd
        }
