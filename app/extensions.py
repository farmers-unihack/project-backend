from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from pymongo.database import Database
from flask_login import LoginManager

mongo = PyMongo()
bcrypt = Bcrypt()
login_manager = LoginManager()

def get_db() -> Database:
    if mongo == None or mongo.db == None:
        raise Exception("MongoDB did not initialize correctly")
    return mongo.db
