import traceback
from flask import Blueprint, jsonify
from app.models.user_model import User
from app.services.group_service import GroupService
from app.services.user_service import UserService
from app.services.auth_service import AuthService
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
            user_service.clock_out_for_user(logged_in_user.id)
            group = group_service.find_group_by_user_id(logged_in_user.id)
            total_hours = sum(
                [User(user).get_total_session_time() for user in group.user_details]
            )
            if (
                total_hours
                >= (len(group.collectibles) + 1)
                * PER_COLLECTIBLE_TIME_INCREMENT
            ):
                group_service.add_random_collectible_to_group(logged_in_user.id)
                return jsonify({"msg": "clocked out", "earned collectible": True}), 200
            return jsonify({"msg": "clocked out"}), 200
        except ValueError as e:
            return jsonify({"msg": str(e)}), 400
        except:
            traceback.print_exc()
            return jsonify({"msg": "Internal Server Error"}), 500

    return user_bp
