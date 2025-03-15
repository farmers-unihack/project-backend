from flask import Blueprint, abort, jsonify
from app.models.user_model import User
from app.services.auth_service import AuthService
from app.services.task_service import TaskService
from app.utils.request_checker import safe_json, safe_json_or_default
import traceback


def create_task_bp(task_service: TaskService, auth_service: AuthService) -> Blueprint:
    task_bp = Blueprint("task", __name__)

    @task_bp.route("/create", methods=["POST"])
    @auth_service.protect_with_jwt
    def create_task(current_user: User):
        try:
            task_name = safe_json("task_name")
            task_description = safe_json_or_default("task_description", "")
            task_service.create_task(current_user.id, task_name, task_description)
            return jsonify({"msg": "Task created successfully"}), 201
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            traceback.print_exc()
            abort(500, "Internal Server Error")

    @task_bp.route("/update", methods=["PUT"])
    @auth_service.protect_with_jwt
    def update_task(current_user: User):
        try:
            task_id = safe_json("task_id")
            task_name = safe_json_or_default("task_name", None)
            task_description = safe_json_or_default("task_description", None)
            task_completed = safe_json_or_default("task_completed", None)
            task_service.update_task(
                current_user.id, task_id, task_name, task_description, task_completed
            )
            return jsonify({"msg": "Task updated successfully"}), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            traceback.print_exc()
            abort(500, "Internal Server Error")

    @task_bp.route("/delete", methods=["DELETE"])
    @auth_service.protect_with_jwt
    def delete_task(current_user: User):
        try:
            task_id = safe_json("task_id")
            task_service.delete_task(current_user.id, task_id)
            return jsonify({"msg": "Task deleted successfully"}), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            traceback.print_exc()
            abort(500, "Internal Server Error")

    return task_bp
