from flask import Blueprint, jsonify 

from app.exceptions.auth_exception import AuthException
from app.services.auth_service import AuthService

from app.utils.request_checker import safe_json

import traceback

def create_auth_bp(auth_service: AuthService) -> Blueprint:
    auth_bp = Blueprint('auth', __name__)

    @auth_bp.route('login', methods=['POST'])
    def login():
        username = safe_json("username")
        password = safe_json("password")

        try: 
            login = auth_service.login(username, password)
            user, token = login
            return jsonify({"username": user.username, "token": token}), 201 
        except AuthException:
            return jsonify({ "msg": "Invalid credentails" }), 401 
        except Exception:
            traceback.print_exc()
            return jsonify({ "msg": "Internal server error" }), 500 

    @auth_bp.route('register', methods=['POST'])
    def register():
        username = safe_json("username")
        password = safe_json("password")

        try:
            auth_service.register(username, password)
            return jsonify({ "msg": "Successfully registered the account" }), 200
        except AuthException:
            return jsonify({ "msg": "user with that username already exists" }), 401 
        except Exception:
            traceback.print_exc()
            return jsonify({ "msg": "Internal server error" }), 500 

    @auth_bp.route("/me", methods=['GET'])
    @auth_service.protect_with_jwt
    def me(current_user):
        return jsonify(logged_in_as=current_user.username), 200
    return auth_bp
