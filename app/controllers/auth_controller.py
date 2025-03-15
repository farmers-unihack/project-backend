from flask import Blueprint, jsonify 

from app.exceptions.auth_exception import AuthException
from app.services.auth_service import AuthService

from app.utils.request_checker import safe_json

import traceback

def create_auth_bp(auth_service: AuthService) -> Blueprint:
    auth_bp = Blueprint('auth', __name__)

    @auth_bp.route('login', methods=['POST'])
    def login():
        try: 
            username = safe_json("username")
            password = safe_json("password")
            login = auth_service.login(username, password)
            user, token = login
            return jsonify({"username": user.username, "token": token}), 201 
        except AuthException:
            return jsonify({ "msg": "Invalid credentails" }), 401 
        except ValueError:
            return jsonify({ "msg": "Invalid input" }), 400 
        except Exception:
            traceback.print_exc()
            return jsonify({ "msg": "Internal server error" }), 500 

    @auth_bp.route('register', methods=['POST'])
    def register():
        try:
            username = safe_json("username")
            password = safe_json("password")
            auth_service.register(username, password)
            return jsonify({ "msg": "Successfully registered the account" }), 200
        except AuthException:
            return jsonify({ "msg": "user with that username already exists" }), 401 
        except ValueError:
            return jsonify({ "msg": "Invalid input" }), 400 
        except Exception:
            traceback.print_exc()
            return jsonify({ "msg": "Internal server error" }), 500 
    return auth_bp
