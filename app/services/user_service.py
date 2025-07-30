"""
User Service - Business logic for user operations
"""

from app.models import UserData
from app import db
import uuid

class UserService:
    """Service class for user-related operations"""
    
    @staticmethod
    def create_user(name, email, password):
        """Create a new user"""
        try:
            client_id = str(uuid.uuid1())
            new_user = UserData(
                name=name,
                email=email,
                password=password,
                client_id=client_id
            )
            db.session.add(new_user)
            db.session.commit()
            return True, client_id
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        return UserData.query.filter_by(email=email).first()
    
    @staticmethod
    def get_user_by_client_id(client_id):
        """Get user by client_id"""
        return UserData.query.filter_by(client_id=client_id).first()
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user with email and password"""
        user = UserData.query.filter_by(email=email, password=password).first()
        return user.client_id if user else None
    
    @staticmethod
    def get_user_name(client_id):
        """Get user name by client_id"""
        user = UserData.query.filter_by(client_id=client_id).first()
        return user.name if user else None 