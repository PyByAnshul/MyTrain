"""
Authentication Views - User registration and login
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.services import UserService, EmailService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup')
def signup():
    """Signup page"""
    return render_template('signuppage.html')

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    """User login"""
    email = request.json['email'].strip()
    password = request.json['password'].strip()
    
    client_id = UserService.authenticate_user(email, password)
    
    if client_id is None:
        client_id = ''
    
    return jsonify({'client_id': client_id})

@auth_bp.route('/signupForm', methods=['POST', 'GET'])
def signup_form():
    """Handle signup form submission"""
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    repassword = request.json['repassword']
    
    # Generate OTP
    otp = EmailService.generate_otp()
    
    # Send verification email
    if EmailService.send_verification_email(email, otp):
        return jsonify({'otp': otp, 'email': True})
    
    return jsonify({'email': False})

@auth_bp.route('/verifyOTP', methods=['POST', 'GET'])
def verify_otp():
    """Verify OTP"""
    print(request.json['otp'])
    return redirect(url_for('main.train_finder'))

@auth_bp.route('/signupFormCompleted', methods=['POST'])
def signup_form_completed():
    """Complete user registration"""
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    
    success, result = UserService.create_user(name, email, password)
    
    if success:
        return jsonify({'client_id': result})
    else:
        return jsonify({'error': result}), 400

@auth_bp.route('/user_page/<client_id>')
def user_page(client_id):
    """User dashboard page"""
    username = UserService.get_user_name(client_id)
    return render_template('index.html', username=username, username1='anshul') 