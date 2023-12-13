from flask import Flask
from flask_mongoengine import MongoEngine
app = Flask(__name__)

#setting 
from mytrain.setting import *


@app.route('/')
def train2():
    return 'hello'


