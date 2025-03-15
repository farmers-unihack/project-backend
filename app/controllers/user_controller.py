import traceback
from flask import Blueprint, jsonify
from app.models.user_model import User
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.utils.time import get_current_time

def create_user_bp(user_service: UserService, auth_service: AuthService) -> Blueprint:
    user_bp = Blueprint("user", __name__)

    @user_bp.route("/clockin", methods=["POST"])
    @auth_service.protect_with_jwt
    def clock_in(logged_in_user: User):
        try:
            user_service.clock_in_for_user(logged_in_user.id, get_current_time())
            return jsonify({ "msg": "clocked in" }), 200
        except ValueError as e:
            return jsonify({ "msg": str(e) }), 400
        except:
            traceback.print_exc()
            return jsonify({ "msg": "Internal Server Error" }), 500

    @user_bp.route("/clockout", methods=["POST"])
    @auth_service.protect_with_jwt
    def clock_out(logged_in_user: User):
        try:
            # Todo store session now
            user_service.clock_out_for_user(logged_in_user.id)
            return jsonify({ "msg": "clocked out" }), 200
        except ValueError as e:
            return jsonify({ "msg": str(e) }), 400
        except:
            traceback.print_exc()
            return jsonify({ "msg": "Internal Server Error" }), 500
    return user_bp 
