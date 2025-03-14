from flask import Flask

from app.routes.api import api_bp
from app.routes.auth import auth_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
