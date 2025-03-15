from flask import Blueprint, abort, jsonify
from app.models.user_model import User
from app.services.auth_service import AuthService
from app.services.group_service import GroupService
from app.utils.request_checker import safe_json 
import traceback


def create_group_bp(group_service: GroupService, auth_service: AuthService) -> Blueprint:
    group_bp = Blueprint("group", __name__)

    @group_bp.route("create", methods=["POST"])
    @auth_service.protect_with_jwt
    def create(logged_in_user: User):
        try:
            group_name = safe_json("group_name")
            group_service.create_group(group_name, logged_in_user.id)
            return jsonify({"msg": "Group created successfully"}), 201
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            traceback.print_exc()
            abort(500, "Internal Server Error")

    @group_bp.route("join", methods=["POST"])
    @auth_service.protect_with_jwt
    def join(logged_in_user: User):
        try:
            group_id = safe_json("group_id")
            group_service.add_user_to_group(group_id, logged_in_user.id)
            return jsonify({"msg": "Joined group successfully"}), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            traceback.print_exc()
            abort(500, "Internal Server Error")

    @group_bp.route("users", methods=["GET"])
    @auth_service.protect_with_jwt
    def users(logged_in_user: User):
        try:
            group = group_service.find_group_by_user_id(logged_in_user.id)
            return jsonify(group.user_details), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            traceback.print_exc()
            abort(500, "Internal Server Error")

    @group_bp.route("leave", methods=["POST"])
    @auth_service.protect_with_jwt
    def leave_group(logged_in_user: User):
        try:
            group_service.remove_user_from_group(logged_in_user.id)
            return jsonify({"msg": "Left group successfully"}), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            traceback.print_exc()
            abort(500, "Internal Server Error")

    @group_bp.route("completed_tasks", methods=["GET"])
    def completed_tasks():
        abort(500, "Not Implemented")
        # try:
        #     group_id = request.args.get("group_id")
        #     time_limit = request.args.get("time_limit")
        #     tasks = group_service.get_completed_tasks(group_id, time_limit)
        #     return jsonify(tasks), 200
        # except ValueError as ve:
        #     abort(400, str(ve))
        # except Exception as e:
        #     abort(500, "Internal Server Error")

    return group_bp
