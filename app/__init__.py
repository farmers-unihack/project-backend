from flask import Flask
from flask_pymongo import PyMongo

from app.routes.api import api_bp
from app.routes.auth import auth_bp

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')

    mongo.init_app(app)
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

def get_db():
    return mongo.db