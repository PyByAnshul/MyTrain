from app import app
from flask_mongoengine import MongoEngine
from config import Config
from flask_pymongo import PyMongo
#congiration integraion
app.config.from_object(Config)

#mongo database
dbs = MongoEngine(app)
client=PyMongo(app).db
mydb=client
#import apps here
