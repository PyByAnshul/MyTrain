from flask import Flask,render_template,request,jsonify,redirect,url_for
from flask_mongoengine import MongoEngine
from datetime import datetime
app = Flask(__name__)
import requests
import time
from uuid import uuid1
#setting 
from mytrain.setting import *
from mytrain.model import database_server,get_train,keywordsearch,get_details


@app.route('/')
def train2():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signuppage.html')

@app.route('/signupForm',methods=['POST','GET'])
def signupform():
    print(request.json['name'])
    return 'signup'
@app.route('/verifyOTP',methods=['POST','GET'])
def verifyOTP():
    print(request.json['otp'])
    return redirect(url_for('train_finder'))

@app.route('/train_finder')
def train_finder():
    return render_template('train_finder.html')


@app.route('/submitsearch',methods=['POST','GET'])
def submitsearch():
    toDest=request.json['toDest']
    fromDest=request.json['fromDest']
    date=request.json['toDate']
    to_id=dict(mydb.traindatabase.find_one({'station_name':{"$regex":toDest}}))
    from_id=dict(mydb.traindatabase.find_one({'station_name':{"$regex":fromDest}}))
    print(toDest,fromDest)
    request_id=str(uuid1())
    data=get_train(to_id['station_code'],from_id['station_code'])
    if data==None:
        if date==None or date=='':
            date=datetime.now().date
        url = "https://irctc1.p.rapidapi.com/api/v3/trainBetweenStations"
        querystring = {"fromStationCode": from_id.get('station_code'),"toStationCode":to_id.get('station_code'),"dateOfJourney":f'{date}'}
        headers = {
            "X-RapidAPI-Key": "793a7dc73cmsh5fc4ac4754f7c66p1ca8ebjsn655a0b81d347",
            "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        res=response.json()
        if res.get('status')==True and res.get('message')=='Success':
            data=res.get('data')
            database_server(data,request_id)
            keywordsearch(to_id['station_code'],from_id['station_code'],request_id)
            print('this is from api ')
    return jsonify(list(data))

@app.route('/train_finder/<train_no>')
def searchtrain_no(train_no):
    data=get_details(train_no)
    return f'{data}'