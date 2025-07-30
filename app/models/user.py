"""
User Model
"""

from app import db
from datetime import datetime

class UserData(db.Model):
    """User registration and authentication model"""
    __tablename__ = 'user_data'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserData {self.email}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'client_id': self.client_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 