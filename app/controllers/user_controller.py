import traceback
from flask import Blueprint, jsonify
from app.models.user_model import User
from app.services.group_service import GroupService
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.group_service import GroupService
from app.utils.request_checker import safe_json_or_default
from app.utils.time import get_current_time
from app.static.collectibles import PER_COLLECTIBLE_TIME_INCREMENT, ALL_COLLECTIBLES


def create_user_bp(
    user_service: UserService, auth_service: AuthService, group_service: GroupService
) -> Blueprint:

    user_bp = Blueprint("user", __name__)

    @user_bp.route("/clockin", methods=["POST"])
    @auth_service.protect_with_jwt
    def clock_in(logged_in_user: User):
        try:
            user_service.clock_in_for_user(logged_in_user.id, get_current_time())
            return jsonify({"msg": "clocked in"}), 200
        except ValueError as e:
            return jsonify({"msg": str(e)}), 400
        except:
            traceback.print_exc()
            return jsonify({"msg": "Internal Server Error"}), 500

    @user_bp.route("/clockout", methods=["POST"])
    @auth_service.protect_with_jwt
    def clock_out(logged_in_user: User):
        try:
            # Todo store session now
            keystroke_cnt = safe_json_or_default("wordCount", None)
            mouse_click_cnt = safe_json_or_default("clickCount", None)
            valid = bool(safe_json_or_default("valid", "False"))
            user_service.clock_out_for_user(
                logged_in_user.id, keystroke_cnt, mouse_click_cnt, valid
            )
            group = group_service.find_group_by_user_id(logged_in_user.id)
            total_hours = sum(
                [User(user).get_total_session_time() for user in group.user_details]
            )
            if (
                total_hours
                >= (len(group.collectibles) + 1) * PER_COLLECTIBLE_TIME_INCREMENT
            ):
                group_service.add_random_collectible_to_group(logged_in_user.id)
                return jsonify({"msg": "clocked out", "earned_collectible": True}), 200
            return jsonify({"msg": "clocked out"}), 200
        except ValueError as e:
            return jsonify({"msg": str(e)}), 400
        except:
            traceback.print_exc()
            return jsonify({"msg": "Internal Server Error"}), 500

    @user_bp.route("/me", methods=["GET"])
    @auth_service.protect_with_jwt
    def me(logged_in_user: User):
        data = {
            "username": logged_in_user.username,
            "in_group": False,
        }

        try:
            group = group_service.find_group_by_user_id(logged_in_user.id)
            data["group_name"] = group.name
            data["in_group"] = True
        except:
            pass

        return jsonify(data), 200

    return user_bp
