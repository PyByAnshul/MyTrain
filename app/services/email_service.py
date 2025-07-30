"""
Email Service - Business logic for email operations
"""

from flask_mail import Message
from app import mail
import random

class EmailService:
    """Service class for email-related operations"""
    
    @staticmethod
    def send_verification_email(user_email, otp):
        """Send OTP verification email"""
        try:
            msg = Message(
                'MyTrain - Email Verification',
                sender='a9756549615@gmail.com',
                recipients=[user_email]
            )
            msg.body = f'Hello from MyTrain app! Your verification code is: {otp}'
            
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Error sending verification email: {e}")
            return False
    
    @staticmethod
    def send_booking_confirmation_email(email, qr_path):
        """Send booking confirmation email with QR code"""
        try:
            msg = Message(
                'MyTrain - Booking Confirmation',
                sender='a9756549615@gmail.com',
                recipients=[email]
            )
            msg.body = 'Your booking has been confirmed. Please find your QR code attached.'
            
            # Attach QR code
            with open(qr_path, 'rb') as qr_file:
                msg.attach(
                    qr_path.split('/')[-1],
                    'image/png',
                    qr_file.read()
                )
            
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Error sending booking confirmation email: {e}")
            return False
    
    @staticmethod
    def generate_otp():
        """Generate a 4-digit OTP"""
        return str(random.randint(1000, 9999))
    
    @staticmethod
    def send_password_reset_email(email, reset_token):
        """Send password reset email"""
        try:
            msg = Message(
                'MyTrain - Password Reset',
                sender='a9756549615@gmail.com',
                recipients=[email]
            )
            msg.body = f'Your password reset token is: {reset_token}'
            
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Error sending password reset email: {e}")
            return False 