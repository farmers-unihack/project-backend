from typing import Any
from flask import Flask
from flask_session import Session

def create_app() -> Any:

    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)

    from app.config import Config
    app.config.from_object(Config)

    from app.extensions import mongo, bcrypt, login_manager
    mongo.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    Session(app)

    from app.routes.api import api_bp
    from app.routes.auth import auth_bp
    from app.routes.group import group_bp
    from app.routes.group_invite import group_invite_bp

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(group_bp, url_prefix="/group")
    app.register_blueprint(group_invite_bp, url_prefix="/invite")


    from app.models.user_model import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.find_by_id(user_id)

    return app