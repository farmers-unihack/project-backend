from flask import Blueprint, abort, jsonify, request
from app.services.group_service import GroupService


def create_group_bp(group_service: GroupService):
    group_bp = Blueprint("group", __name__)

    @group_bp.route("create", methods=["POST"])
    def create():
        try:
            group_name = request.json["group_name"]
            group_service.create_group(group_name)
            return jsonify({"msg": "Group created successfully"}), 201
        except ValueError as ve:
            abort(400, str(ve))
        except Exception as e:
            print(e)
            abort(500, "Internal Server Error")

    @group_bp.route("join", methods=["POST"])
    def join():
        try:
            user_id = request.json["user_id"]
            group_id = request.json["group_id"]
            group_service.add_user_to_group(user_id, group_id)
            return jsonify({"msg": "Joined group successfully"}), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception as e:
            abort(500, "Internal Server Error")

    @group_bp.route("users", methods=["GET"])
    def users():
        try:
            group_id = request.args.get("group_id")
            group = group_service.find_group_by_id(group_id)
            return jsonify(group["users"]), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception as e:
            abort(500, "Internal Server Error")

    @group_bp.route("leave", methods=["POST"])
    def leave_group():
        try:
            user_id = request.json["user_id"]
            group_id = request.json["group_id"]
            group_service.remove_user_from_group(user_id, group_id)
            return jsonify({"msg": "Left group successfully"}), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception as e:
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
