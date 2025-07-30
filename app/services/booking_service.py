"""
Booking Service - Business logic for booking operations
"""

from app.models import Booking
from app import db
import qrcode
import os
from datetime import datetime

class BookingService:
    """Service class for booking-related operations"""
    
    @staticmethod
    def create_booking(booking_data, qr_codes_dir):
        """Create a new booking with QR code"""
        try:
            # Generate QR code data
            qr_data = f"Name: {booking_data['name']}\nEmail: {booking_data['email']}\nPhone: {booking_data['phone']}\nAddress: {booking_data['address']}\nTrain No: {booking_data['train_no']}\nCoach No: {booking_data['coach_no']}\nSeats: {booking_data['seats']}\nTotal Price: {booking_data['total_price']}\nCoach Type: {booking_data['coach_type']}"
            
            # Generate QR code filename
            qr_filename = f"{booking_data['phone']}_{booking_data['train_no']}.png"
            qr_path = os.path.join(qr_codes_dir, qr_filename)
            
            # Create QR code
            qr = qrcode.make(qr_data)
            qr.save(qr_path)
            
            # Create booking record
            new_booking = Booking(
                name=booking_data['name'],
                email=booking_data['email'],
                phone=booking_data['phone'],
                address=booking_data['address'],
                train_no=booking_data['train_no'],
                coach_no=booking_data['coach_no'],
                seats=booking_data['seats'],
                total_price=float(booking_data['total_price']),
                coach_type=booking_data['coach_type'],
                qr_filename=qr_filename
            )
            
            db.session.add(new_booking)
            db.session.commit()
            
            return True, {
                'booking_id': new_booking.id,
                'qr_filename': qr_filename,
                'qr_path': qr_path
            }
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_booking_by_id(booking_id):
        """Get booking by ID"""
        return Booking.query.get(booking_id)
    
    @staticmethod
    def get_bookings_by_email(email):
        """Get all bookings for a user"""
        return Booking.query.filter_by(email=email).order_by(Booking.booking_date.desc()).all()
    
    @staticmethod
    def get_bookings_by_train(train_no):
        """Get all bookings for a specific train"""
        return Booking.query.filter_by(train_no=train_no).order_by(Booking.booking_date.desc()).all()
    
    @staticmethod
    def get_recent_bookings(limit=10):
        """Get recent bookings"""
        return Booking.query.order_by(Booking.booking_date.desc()).limit(limit).all()
    
    @staticmethod
    def cancel_booking(booking_id):
        """Cancel a booking (soft delete)"""
        try:
            booking = Booking.query.get(booking_id)
            if booking:
                # For now, we'll just delete the booking
                # In a real application, you might want to mark it as cancelled instead
                db.session.delete(booking)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            return False 