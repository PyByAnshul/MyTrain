# config.py

import os

class Config:
    DEBUG = True
    SECRET_KEY = 'anshulkumar@#$^&dipanshu@@chirag@#$#adnan####@$#'
    SESSION_COOKIE_SECURE=True
    
    # SQLite Database Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'mytrain.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email Configuration
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USERNAME='a9756549615@gmail.com'
    MAIL_PASSWORD='pnzaieubovsihewz'
    MAIL_USE_TLS=False
    MAIL_USE_SSL=True
    MAIL_RECIPIENTS=['a9456954582@gmail.com']
    # other configurations...
