from app import app
from config import Config
from pymongo import MongoClient
from flask_mail import Mail

#congiration integraion
app.config.from_object(Config)

#mongo database
# dbs = MongoEngine(app)
client=client = MongoClient('mongodb://root:example@mongo:27017/')
mydb = client['mytrain']

################ intialize mail app ##############
mail = Mail(app)
