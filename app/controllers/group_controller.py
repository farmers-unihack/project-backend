from datetime import timedelta
from flask import Blueprint, abort, jsonify, request
from app.models.task_model import Task
from app.services.group_service import GroupService
from app.utils.request_checker import safe_json
import traceback


def create_group_bp(group_service: GroupService) -> Blueprint:
    group_bp = Blueprint("group", __name__)

    @group_bp.route("create", methods=["POST"])
    def create():
        try:
            group_name = safe_json("group_name")
            user_id = safe_json("user_id")
            group_service.create_group(group_name, user_id)
            return jsonify({"msg": "Group created successfully"}), 201
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            traceback.print_exc()
            abort(500, "Internal Server Error")

    @group_bp.route("join", methods=["POST"])
    def join():
        try:
            user_id = safe_json("user_id")
            group_id = safe_json("group_id")
            group_service.add_user_to_group(user_id, group_id)
            return jsonify({"msg": "Joined group successfully"}), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            traceback.print_exc()
            abort(500, "Internal Server Error")

    @group_bp.route("users", methods=["GET"])
    def users():
        try:
            group_id = request.args.get("group_id")
            group = group_service.find_group_by_id(group_id)
            return jsonify(group.users), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            traceback.print_exc()
            abort(500, "Internal Server Error")

    @group_bp.route("leave", methods=["POST"])
    def leave_group():
        try:
            user_id = safe_json("user_id")
            group_id = safe_json("group_id")
            group_service.remove_user_from_group(user_id, group_id)
            return jsonify({"msg": "Left group successfully"}), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            traceback.print_exc()
            abort(500, "Internal Server Error")

    @group_bp.route("recent_completed_tasks", methods=["GET"])
    def recent_completed_tasks():
        try:
            group_id = safe_json("group_id")
            time_limit = timedelta(**safe_json("time_limit"))
            group_tasks: list[Task] = group_service.get_group_tasks(group_id)
            filtered_tasks = filter(
                lambda task: task.is_completed_within_recent_time(time_limit),
                group_tasks,
            )
            return jsonify(map(lambda task: task.to_dict(), filtered_tasks)), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            traceback.print_exc()
            abort(500, "Internal Server Error")

    return group_bp
