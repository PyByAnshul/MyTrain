"""
MyTrain - Railway Information & Booking System
Flask Application Factory
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
from .utils.proxy_manager import monkey_patch_requests
# Initialize extensions
db = SQLAlchemy()
mail = Mail()

monkey_patch_requests()
def create_app(config_class=None):
    """Application factory function"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    if config_class:
        app.config.from_object(config_class)
    else:
        from config import Config
        app.config.from_object(Config)
    
    # Initialize extensions with app
    db.init_app(app)
    mail.init_app(app)
    
    # Ensure directories exist
    ensure_directories(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

def ensure_directories(app):
    """Ensure required directories exist"""
    qr_codes_dir = os.path.join(app.static_folder, 'qr_codes')
    if not os.path.exists(qr_codes_dir):
        os.makedirs(qr_codes_dir)

def register_blueprints(app):
    """Register Flask blueprints"""
    from app.views.main import main_bp
    from app.views.auth import auth_bp
    from app.views.trains import trains_bp
    from app.views.booking import booking_bp
    from app.api.routes import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(trains_bp, url_prefix='/trains')
    app.register_blueprint(booking_bp, url_prefix='/booking')
    app.register_blueprint(api_bp, url_prefix='/api')

def register_error_handlers(app):
    """Register error handlers"""
    from app.views.errors import register_error_handlers as register_errors
    register_errors(app) 