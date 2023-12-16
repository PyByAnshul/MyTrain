from app import app
from flask_mongoengine import MongoEngine
from config import Config
from json import JSONEncoder
from flask_pymongo import PyMongo
#congiration integraion
app.config.from_object(Config)

#mongo database
db = MongoEngine(app)
mydb=PyMongo(app)
#import apps here
from searchtrain.searchtrain import searchtrain
### register apps here
app.register_blueprint(searchtrain)
