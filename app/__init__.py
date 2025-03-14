from typing import Any
from flask import Flask
<<<<<<< HEAD
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

from app.routes.api import api_bp
from app.routes.auth import auth_bp

<<<<<<< HEAD
bcrypt = Bcrypt()
=======
from app.config import Config

>>>>>>> 686dd07 (Added config class and dotenv)
mongo = PyMongo()
bcrypt = Bcrypt()

def create_app():
=======
from flask_session import Session

def create_app() -> Any:
>>>>>>> 7401bac (Authentication and sessions)
    app = Flask(__name__)

    from app.config import Config
    app.config.from_object(Config)

<<<<<<< HEAD
    bcrypt.init_app(app)
=======
    from app.extensions import mongo, bcrypt, login_manager
>>>>>>> 7401bac (Authentication and sessions)
    mongo.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    Session(app)

    from app.routes.api import api_bp
    from app.routes.auth import auth_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')


    from app.models.user_model import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.find_by_id(user_id)

    return app
