from flask import Blueprint, abort, jsonify
from app.services.task_service import TaskService
from app.utils.request_checker import safe_json, safe_json_or_default


def create_tasks_bp(task_service: TaskService) -> Blueprint:
    tasks_bp = Blueprint("tasks", __name__)

    @tasks_bp.route("/create", methods=["POST"])
    def create_task():
        try:
            task_name = safe_json("task_name")
            task_description = safe_json_or_default("task_description", "")
            task_service.create_task(task_name, task_description)
            return jsonify({"msg": "Task created successfully"}), 201
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            abort(500, "Internal Server Error")

    @tasks_bp.route("/update", methods=["PUT"])
    def update_task():
        try:
            task_id = safe_json("task_id")
            task_name = safe_json_or_default("task_name", None)
            task_description = safe_json_or_default("task_description", None)
            task_completed = safe_json_or_default("task_completed", None)
            task_service.update_task(
                task_id, task_name, task_description, task_completed
            )
            return jsonify({"msg": "Task updated successfully"}), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            abort(500, "Internal Server Error")

    @tasks_bp.route("/delete", methods=["DELETE"])
    def delete_task():
        try:
            task_id = safe_json("task_id")
            task_service.delete_task(task_id)
            return jsonify({"msg": "Task deleted successfully"}), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            abort(500, "Internal Server Error")

    return tasks_bp
