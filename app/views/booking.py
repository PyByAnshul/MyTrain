"""
Booking Views - Ticket booking functionality
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from app.services import BookingService, EmailService, TrainService
import os

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/book_ticket/')
def book():
    """Booking page"""
    train_no = request.args.get('train_no')
    start_from = request.args.get('start_from')
    end_from = request.args.get('end_from')
    
    station_info = TrainService.check_train_exists(train_no)
    
    return render_template('bookingpage.html',
                         train_no=train_no,
                         fromDest=start_from, 
                         toDest=end_from)

@booking_bp.route('/book/book_ticket', methods=['GET','POST'])
def booking_link():
    """Handle booking form submission"""
    if request.method == 'GET':
        train_no = request.args.get('trainno')
        coach_no = request.args.get('coachno')
        seats = request.args.get('seats')
        total_price = request.args.get('totalprice')
        coach_type = request.args.get('coachtype')

        return render_template('user_info.html',
                             train_no=train_no,
                             coach_no=coach_no,
                             seats=seats,
                             total_price=total_price,
                             coach_type=coach_type)

    if request.method == 'POST':
        # Get form data
        booking_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': '+91' + str(request.form.get('phone')),
            'address': request.form.get('address'),
            'train_no': request.form.get('train_no'),
            'coach_no': request.form.get('coach_no'),
            'seats': request.form.get('seats'),
            'total_price': request.form.get('total_price'),
            'coach_type': request.form.get('coach_type')
        }
        
        # Get QR codes directory
        qr_codes_dir = os.path.join(current_app.static_folder, 'qr_codes')
        
        # Create booking
        success, result = BookingService.create_booking(booking_data, qr_codes_dir)
        
        if success:
            # Send confirmation email
            EmailService.send_booking_confirmation_email(
                booking_data['email'], 
                result['qr_path']
            )
            
            return render_template('success.html', 
                                 name=booking_data['name'],
                                 email=booking_data['email'],
                                 phone=booking_data['phone'],
                                 address=booking_data['address'],
                                 train_no=booking_data['train_no'],
                                 coach_no=booking_data['coach_no'],
                                 seats=booking_data['seats'],
                                 total_price=booking_data['total_price'],
                                 coach_type=booking_data['coach_type'],
                                 qr_path=result['qr_path'],
                                 qr_name=result['qr_filename'])
        else:
            return jsonify({'error': result}), 400

@booking_bp.route('/qr_code')
def qr_code():
    """Serve QR code image"""
    from flask import send_file
    return send_file('static/qr_code.png', mimetype='image/png') 