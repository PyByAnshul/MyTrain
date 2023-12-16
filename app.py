from flask import Flask,render_template
from flask_mongoengine import MongoEngine
app = Flask(__name__)

#setting 
from mytrain.setting import *


@app.route('/')
def train2():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('loginpage.html')


@app.route('/train_finder')
def train_finder():
    return render_template('train_finder.html')


