from app import app
from flask_mongoengine import MongoEngine
from config import Config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://a9756549615:oNOccgAMhlA79wHW@cluster0.mak8f9p.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

#congiration integraion

app.config.from_object(Config)
#mongo database
dbs = MongoEngine(app)

mydb=client.mytrain
#import apps here
