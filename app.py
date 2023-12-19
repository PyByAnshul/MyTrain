from flask_mail import Message
import random
from uuid import uuid1
import time
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_mongoengine import MongoEngine
from datetime import datetime
app = Flask(__name__)
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


@app.route('/')
def train2():
    return render_template('index.html')


@app.route('/signup')
def signup():
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


@app.route('/train_finder')
def train_finder():
    return render_template('train_finder.html')


@app.route('/submitsearch', methods=['POST', 'GET'])
def submitsearch():
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
            date = datetime.now().date
        url = "https://irctc1.p.rapidapi.com/api/v3/trainBetweenStations"
        querystring = {"fromStationCode": from_id.get(
            'station_code'), "toStationCode": to_id.get('station_code'), "dateOfJourney": f'{date}'}
        headers = {
            "X-RapidAPI-Key": "793a7dc73cmsh5fc4ac4754f7c66p1ca8ebjsn655a0b81d347",
            "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        res = response.json()
        if res.get('status') == True and res.get('message') == 'Success':
            data = res.get('data')
            database_server(data, request_id)
            keywordsearch(to_id['station_code'],
                          from_id['station_code'], request_id)
            print('this is from api ')
    return jsonify(list(data))


@app.route('/train_finder/<train_no>')
def searchtrain_no(train_no):
    data = get_details(train_no)
    return f'{data}'


@app.route('/user_page/<client_id>')
def home_page(client_id):
    return render_template('index.html', username=get_user_name(client_id), username1='anshul')
