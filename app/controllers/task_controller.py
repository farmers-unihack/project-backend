from flask import Blueprint, abort, jsonify, request
from app.services.task_service import TaskService
from app.utils.request_checker import request_json_contains


def create_tasks_bp(task_service: TaskService) -> Blueprint:
    tasks_bp = Blueprint("tasks", __name__)

    @task_bp.route("/create", methods=["POST"])
    def create_task():
        try:
            if not request_json_contains(["task_name"]):
                abort(400, "Invalid request body")
            task_name = request.json["task_name"]
            task_description = request.json.get("task_description", "")
            task_service.create_task(task_name, task_description)
            return jsonify({"msg": "Task created successfully"}), 201
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            abort(500, "Internal Server Error")

    @task_bp.route("/update", methods=["PUT"])
    def update_task():
        try:
            if not request_json_contains(["task_id"]):
                abort(400, "Invalid request body")
            task_id = request.json["task_id"]
            task_name = request.json.get("task_name", None)
            task_description = request.json.get("task_description", None)
            task_completed = request.json.get("task_completed", None)
            task_service.update_task(
                task_id, task_name, task_description, task_completed
            )
            return jsonify({"msg": "Task updated successfully"}), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            abort(500, "Internal Server Error")

    @task_bp.route("/delete", methods=["DELETE"])
    def delete_task():
        try:
            if not request_json_contains(["task_id"]):
                abort(400, "Invalid request body")
            task_id = request.json["task_id"]
            task_service.delete_task(task_id)
            return jsonify({"msg": "Task deleted successfully"}), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            abort(500, "Internal Server Error")

    return tasks_bp