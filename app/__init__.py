from typing import Any
from flask import Flask

from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

mongo = PyMongo()
bcrypt = Bcrypt()

def create_app() -> Any:
    app = Flask(__name__)

    from flask_cors import CORS 
    CORS(app)

    from app.config import Config
    app.config.from_object(Config)

    # Initialize Extensions
    mongo.init_app(app)
    bcrypt.init_app(app)

    if mongo.db == None:
        raise RuntimeError("MongoDB failed to connect")

    from app.controllers import register_controllers
    register_controllers(app, mongo.db, bcrypt)

    return app
