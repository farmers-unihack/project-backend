from bson import ObjectId
from flask import Blueprint, abort, app, jsonify, request

from app.models.group_model import GroupModel

group_bp = Blueprint("group", __name__)
group_model = GroupModel()


@group_bp.route("create", methods=["POST"])
def create():
    try:
        group_name = request.json["group_name"]
        group_model.create_group(group_name)
        return jsonify({"msg": "Group created successfully"}), 200
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, "Internal Server Error")


@group_bp.route("join", methods=["POST"])
def join():
    try:
        user_id = request.json["user_id"]
        group_id = request.json["group_id"]
        group_model.add_user(user_id, group_id)
        return jsonify({"msg": "Joined group successfully"}), 200
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, "Internal Server Error")


@group_bp.route("users", methods=["GET"])
def users():
    try:
        group_id = request.args.get("group_id")
        group = group_model.get_group(group_id)
        users = group["users"]
        return jsonify(users), 200
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, "Internal Server Error")


@group_bp.route("leave", methods=["POST"])
def leave_group():
    try:
        user_id = request.json["user_id"]
        group_id = request.json["group_id"]
        group_model.remove_user(user_id, group_id)
        return jsonify({"msg": "Left group successfully"}), 200
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, "Internal Server Error")


@group_bp.route("completed_tasks", methods=["GET"])
def completed_tasks():
    try:
        group_id = request.args.get("group_id")
        time_limit = request.args.get("time_limit")
        tasks = group_model.get_completed_tasks(group_id, time_limit)
        return jsonify(tasks), 200
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, "Internal Server Error")
