# config.py

class Config:
    DEBUG = True
    SECRET_KEY = 'anshulkumar@#$^&dipanshu@@chirag@#$#adnan####@$#'
    SESSION_COOKIE_SECURE=True
   # MONGODB_SETTINGS={'host':'mongodb://localhost:27017/mytrain'}
   # MONGO_URI='mongodb://localhost:27017/mytrain'
     MONGODB_SETTINGS={'host':'mongodb+srv://a9756549615:oNOccgAMhlA79wHW@cluster0.mak8f9p.mongodb.net/mytrain?retryWrites=true&w=majority'}
     MONGO_URI='mongodb+srv://a9756549615:oNOccgAMhlA79wHW@cluster0.mak8f9p.mongodb.net/mytrain?retryWrites=true&w=majority'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USERNAME='a9756549615@gmail.com'
    MAIL_PASSWORD='pnzaieubovsihewz'
    MAIL_USE_TLS=False
    MAIL_USE_SSL=True
    MAIL_RECIPIENTS=['a9456954582@gmail.com']
    # other configurations...
