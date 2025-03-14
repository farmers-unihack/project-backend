from flask import Flask

from flask_pymongo import PyMongo

from app.config import Config

mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)

    from app.routes.api import api_bp
    from app.routes.auth import auth_bp
    from app.routes.group import group_bp

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(group_bp, url_prefix="/group")

    return app


def get_db():
    return mongo.db
