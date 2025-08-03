"""
Proxy Model
"""
from app import db
from datetime import datetime

class ProxyStatus(db.Model):
    __tablename__ = 'proxy_status'
    
    id = db.Column(db.Integer, primary_key=True)
    proxy = db.Column(db.String(50), unique=True, nullable=False)
    last_used_time = db.Column(db.DateTime, nullable=True)
    is_working = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<ProxyStatus {self.proxy}>'