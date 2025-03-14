from flask import Flask
from flask_bcrypt import Bcrypt

from app.routes.api import api_bp
from app.routes.auth import auth_bp

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    bcrypt.init_app(app)

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
