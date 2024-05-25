from flask_mail import Message
import random
from uuid import uuid1
import time
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for,send_file
import qrcode
# import pywhatkit

from flask_mongoengine import MongoEngine
from datetime import datetime
from scripts.trainman import main as trainmanmain
from scripts.indiarailway import main as indiatrain
from scripts.trainstatus import main as trainstatus
from scripts.runningstatus import main as running_status
app = Flask(__name__)
import os
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
QR_CODES_DIR = os.path.join(STATIC_DIR, 'qr_codes')

# Ensure the qr_codes directory exists
if not os.path.exists(QR_CODES_DIR):
    os.makedirs(QR_CODES_DIR)
# setting
if app:
    from mytrain.setting import *
    from mytrain.model import database_server, get_train, keywordsearch, get_details, user_singin, get_user_name,get_user_id


def send_mails(user_email, otp):
    msg = Message(f'no-reply @#MyTrain app', sender='a9756549615@gmail.com',
                  recipients=[user_email], body=f'hii from MyTrain app your varification code is {otp}')
    try:
        mail.send(msg)
        return True
    except Exception as e:
        # Log the error
        print(e)
        return False

def send_email_with_qr(email, qr_path):
    msg = Message('Your QR code for booking details', sender='a9756549615@gmail.com', recipients=[email])
    with app.open_resource(qr_path) as qr_file:
        msg.attach(qr_path.split('/')[-1], 'image/png', qr_file.read())
    try:
        mail.send(msg)
        return True
    except Exception as e:
        # Log the error
        print(e)
        return False

@app.route('/')
def train2():
    return render_template('index.html')


@app.route('/signup')
def signup():
    # print('sing page')
    return render_template('signuppage.html')

@app.route('/login',methods=['POST', 'GET'])
def login():
    email = request.json['email'].strip()
    password = request.json['password'].strip()
    print(email,password)
    client_id_res=get_user_id(email,password)
    print(client_id_res)
    if client_id_res==None:
        client_id_res=''
    return jsonify({'client_id':client_id_res})
    
    


@app.route('/signupForm', methods=['POST', 'GET'])
def signupform():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    repassword = request.json['repassword']
    otp = str(random.random())[-4::]
    if send_mails(email, otp=otp):
        return jsonify({'otp': otp, 'email': True})
    return jsonify({'email': False})


@app.route('/verifyOTP', methods=['POST', 'GET'])
def verifyOTP():
    print(request.json['otp'])
    return redirect(url_for('train_finder'))


@app.route('/signupFormCompleted', methods=['POST'])
def signupFormCompleted():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    client_id = str(uuid1())
    dic = {'name': name, 'email': email,
           'password': password, 'client_id': client_id}
    user_singin(dic)
    return jsonify({'client_id': client_id})

import traceback
@app.route('/train_finder')
def train_finder():
    return render_template('train_finder.html')

@app.route('/find_trains',methods=['POST','GET'])
@app.route('/submitsearch', methods=['POST', 'GET'])
def submitsearch():
    try:
        if request.path.startswith('/find_trains'):
            toDest = request.form.get('toDest')
            fromDest = request.form.get('fromDest')
            date = request.form.get('toDate')
        else:
            toDest = request.json['toDest']
            fromDest = request.json['fromDest']
            date = request.json['toDate']
        to_id = dict(mydb.traindatabase.find_one(
            {'station_name': {"$regex": toDest}}))
        from_id = dict(mydb.traindatabase.find_one(
            {'station_name': {"$regex": fromDest}}))
        print(toDest, fromDest)
        request_id = str(uuid1())
        data = get_train(to_id['station_code'], from_id['station_code'])
        if data == None:
            if date == None or date == '':
                date = datetime.now().date()
                dic=indiatrain(to_id['station_code'],from_id['station_code'],date)
            else:
                dic=indiatrain(to_id['station_code'],from_id['station_code'],date)
            data=dic['train_between_stations']
            if dic.get('status')!=200:
                data=['no data' for i in range(10)]
            
            database_server(data,request_id=request_id)
            keywordsearch(to_id['station_code'],from_id['station_code'],reqest_id=request_id)
        if request.path.startswith('/find_trains'):
            print('find the train',data)
            return render_template('train_finder.html',data=data,fromDest=fromDest,toDest=toDest)
        return jsonify(list(data))
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(['no data' for i in range(10)])



@app.route('/train_finder/<train_no>')
def searchtrain_no(train_no):
    data = running_status(trian_number=train_no,date=datetime.now().date())
    print(data)
    return render_template('running_status.html',table=data,train_no=train_no)


@app.route('/user_page/<client_id>')
def home_page(client_id):
    return render_template('index.html', username=get_user_name(client_id), username1='anshul')


@app.route('/trainstatus')
def trainstatus():
    return render_template('running_status.html',form=True)


@app.route('/get_ticket/<train_no>')
def get_ticker(train_no):
    return render_template('ticket.html')

@app.route('/book')
def book():
    return render_template('bookingpage.html')


@app.route('/book/book_ticket', methods=['GET','POST'])
def booking_link():
    if request.method == 'GET':
        train_no = request.args.get('trainno')
        coach_no = request.args.get('coachno')
        seats = request.args.get('seats')
        total_price = request.args.get('totalprice')
        coach_type = request.args.get('coachtype')

        booking_details = {
            'train_no': train_no,
            'coach_no': coach_no,
            'seats': seats,
            'total_price': total_price,
            'coach_type': coach_type
        }

        # Constructing the booking link
        booking_link = f"/book?trainno={train_no}&coachno={coach_no}&seats={seats}&totalprice={total_price}&coachtype={coach_type}"
        
        return render_template('user_info.html',train_no=train_no,coach_no=coach_no,seats=seats,total_price=total_price,coach_type=coach_type)

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = '+91' + str(request.form.get('phone'))  # Assuming phone numbers start with '+91'
        address = request.form.get('address')
        train_no = request.form.get('train_no')
        coach_no = request.form.get('coach_no')
        seats = request.form.get('seats')
        total_price = request.form.get('total_price')
        coach_type = request.form.get('coach_type')
        
        # Generate the QR code data
        qr_data = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nAddress: {address}\nTrain No: {train_no}\nCoach No: {coach_no}\nSeats: {seats}\nTotal Price: {total_price}\nCoach Type: {coach_type}"
        
        # Save the QR code image with a filename based on phone number and train number
        qr_filename = f"{phone}_{train_no}.png"
        qr_path = os.path.join(QR_CODES_DIR, qr_filename)
        qr = qrcode.make(qr_data)
        qr.save(qr_path)

        # Send the QR code image via WhatsApp
        # pywhatkit.sendwhats_image(phone, qr_path, "Your QR code for booking details")
        send_email_with_qr(email,qr_path)
        # Render the success page with the form data
        return render_template('success.html', name=name, email=email, phone=phone, address=address, 
                               train_no=train_no, coach_no=coach_no, seats=seats, total_price=total_price, 
                               coach_type=coach_type, qr_path=qr_path)
@app.route('/qr_code')
def qr_code():
    # Serve the QR code image to the webpage
    return send_file('static/qr_code.png', mimetype='image/png')


