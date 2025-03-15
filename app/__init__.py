from typing import Any
from flask import Flask

from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session

mongo = PyMongo()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app() -> Any:
    app = Flask(__name__)

    from app.config import Config
    app.config.from_object(Config)

    # Initialize Extensions
    mongo.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    Session(app)

    if mongo.db == None:
        raise RuntimeError("MongoDB failed to connect")

    from app.controllers import register_controllers
    register_controllers(app, mongo.db, bcrypt, login_manager)

    return app
