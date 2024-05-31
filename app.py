from flask_mail import Message
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from datetime import datetime
import qrcode
from uuid import uuid1
import random
from scripts.indiarailway import main as indiatrain
from scripts.runningstatus import main as running_status
from static.stationdata import stations as stations_stored
from scripts.railyatri import main as railyatri_status
from scripts.map import main as map_main
from threading import Thread
import concurrent.futures
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
    from mytrain.model import database_server, get_train, keywordsearch, get_details, user_singin, get_user_name,get_user_id,store_train_data


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

@app.route('/find_trains', methods=['POST', 'GET'])
@app.route('/submitsearch', methods=['POST', 'GET'])
def submitsearch():
    try:
        if request.path.startswith('/find_trains'):
            toDest = request.form.get('toDest')
            fromDest = request.form.get('fromDest')
            date = request.form.get('toDate')
        else:
            data_json = request.json
            toDest = request.json['toDest']
            fromDest = request.json['fromDest']
            date = request.json['toDate']

        # Query the database to find station codes
        to_document = mydb.traindatabase.find_one({'station_name': {"$regex": toDest}})
        from_document = mydb.traindatabase.find_one({'station_name': {"$regex": fromDest}})

        if to_document is None or from_document is None:
            raise ValueError("Invalid station names provided")

        to_id = to_document['station_code']
        from_id = from_document['station_code']

        print(toDest, fromDest)
        request_id = str(uuid1())

        # Retrieve train data
        data = get_train(from_id, to_id)

        if data is None:
            if not date:
                date = datetime.now().date()
            dic = indiatrain(from_id, to_id, date)
            data = dic.get('train_between_stations', [])
            if dic.get('status') != 200:
                data = ['no data' for _ in range(10)]

            # Save data to database
            database_server(data, request_id=request_id)
            keywordsearch(from_id, to_id,request_id)

        if request.path.startswith('/find_trains'):
            # print('find the train', data)
            return render_template('train_finder.html', data=data, fromDest=fromDest, toDest=toDest)
        return jsonify(data)

    except ValueError as ve:
        print(ve)
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500



@app.route('/train_finder/')
def searchtrain_no():
    # Define functions to fetch data
    train_no = request.args.get('train_no')
    fromDest = request.args.get('start_from')
    toDest = request.args.get('end_from')

    def fetch_map(train_no):
        return map_main(train_no)

    def fetch_running_status(train_no):
        return running_status(train_number=train_no, date=datetime.now().date())
    
    def fetch_time_table(train_no):
        return railyatri_status(train_no)
    # Create threads to fetch data concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        running_train_data = executor.submit(fetch_running_status,train_no)
        # time_table_data=executor.submit(fetch_time_table,train_no)
        map_data = executor.submit(fetch_map,train_no)
   

    # Wait for threads to finish and get results
    map_result = map_data.result()
    status_result = running_train_data.result()
    # time_table_result=time_table_data.result()
    # Pass results to the template
    return render_template('running_status.html', running_status=status_result, train_no=train_no, map=map_result,fromDest=fromDest, toDest=toDest)

@app.route('/book_food/')
def book_food():
    # Define functions to fetch data
    train_no = request.args.get('train_no')
    fromDest = request.args.get('start_from')
    toDest = request.args.get('end_from')
    
    time_table_data=railyatri_status(train_no)
      
    return render_template('food_booking.html', train_no=train_no,time_table=time_table_data,fromDest=fromDest, toDest=toDest)

@app.route('/m/link-food-in-train')
def link_food_in_train():
    station_code = request.args.get('station_code')
    train = request.args.get('train')
    return f"Linking food in train for station {station_code} and train {train}"

@app.route('/user_page/<client_id>')
def home_page(client_id):
    return render_template('index.html', username=get_user_name(client_id), username1='anshul')


@app.route('/trainstatus')
def trainstatus():
    return render_template('running_status.html',form=True)




@app.route('/book_ticket/')
def book():
    train_no = request.args.get('train_no')
    start_from = request.args.get('start_from')
    end_from = request.args.get('end_from')
    return render_template('bookingpage.html',train_no=train_no,fromDest=start_from, toDest=end_from)


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
import requests
@app.route('/find_stations',methods=['POST'])
def find_stations():
    station_name=request.json.get('station_name')
    try:
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.7',
            'origin': 'https://www.railyatri.in',
            'priority': 'u=1, i',
            'referer': 'https://www.railyatri.in/',
            '^sec-ch-ua': '^\\^Brave^\\^;v=^\\^125^\\^, ^\\^Chromium^\\^;v=^\\^125^\\^, ^\\^Not.A/Brand^\\^;v=^\\^24^\\^^',
            'sec-ch-ua-mobile': '?0',
            '^sec-ch-ua-platform': '^\\^Windows^\\^^',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }

        params = (
            ('q', station_name),
            ('hide_city', 'true'),
        )

        response = requests.get('https://api.railyatri.in/api/common_city_station_search.json', headers=headers, params=params)
        stations=response.json().get('items')
        station_names = [station['station_name'] for station in stations]
        store_train_data(stations)
    except:
        station_names=stations_stored.suggestions
    return jsonify(station_names)


@app.errorhandler(400)
def bad_request_error(error):
    return render_template('train_error.html')
@app.errorhandler(404)
def bad_request_error(error):
    return render_template('train_error.html')

# Route for 500 - Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('train_error.html')