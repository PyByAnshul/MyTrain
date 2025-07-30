"""
Booking Model
"""

from app import db
from datetime import datetime

class Booking(db.Model):
    """Ticket booking records model"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    train_no = db.Column(db.String(20), nullable=False)
    coach_no = db.Column(db.String(10), nullable=False)
    seats = db.Column(db.String(10), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    coach_type = db.Column(db.String(20), nullable=False)
    qr_filename = db.Column(db.String(200))
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Booking {self.train_no} - {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'train_no': self.train_no,
            'coach_no': self.coach_no,
            'seats': self.seats,
            'total_price': self.total_price,
            'coach_type': self.coach_type,
            'qr_filename': self.qr_filename,
            'booking_date': self.booking_date.isoformat() if self.booking_date else None
        } 