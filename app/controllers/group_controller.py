from typing import Iterable
from typing import Iterable
from flask import Blueprint, abort, jsonify
from app.models.user_model import User
from app.services.auth_service import AuthService
from datetime import datetime, timedelta
from app.models.task_model import Task
from app.services.group_service import GroupService
from app.utils.request_checker import safe_json, safe_json_or_default
from app.static.collectibles import ALL_COLLECTIBLES
import traceback


def create_group_bp(
    group_service: GroupService, auth_service: AuthService
) -> Blueprint:
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
            group_id = safe_json_or_default("group_id", None)
            invite_code = safe_json_or_default("invite_code", None)
            if invite_code:
                group_service.add_user_by_invite(invite_code, logged_in_user.id)
            elif group_id:
                group_service.add_user_to_group(group_id, logged_in_user.id)
            else:
                raise ValueError("Either group_id or invite_code must be provided")
            return jsonify({"msg": "Joined group successfully"}), 200
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            traceback.print_exc()
            abort(500, "Internal Server Error")

    @group_bp.route("invite", methods=["GET"])
    @auth_service.protect_with_jwt
    def details(logged_in_user: User):
        try:
            group = group_service.find_group_by_user_id(logged_in_user.id)
            return jsonify(group.invite_code), 200
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

    @group_bp.route("recent-completed-tasks", methods=["GET"])
    @auth_service.protect_with_jwt
    def recent_completed_tasks(logged_in_user: User):
        try:
            time_limit = timedelta(**safe_json("time_limit"))
            group_tasks: Iterable[Task] = group_service.get_group_tasks(logged_in_user.id)
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

    @group_bp.route("poll", methods=["GET"])
    @auth_service.protect_with_jwt
    def poll(logged_in_user: User):
        try:
            group = group_service.find_group_by_user_id(logged_in_user.id)
            clocked_in_users: list[dict] = []
            total_time = timedelta() 
            group_collectibles = []
            

            for collectible_id in group.collectibles:
                group_collectibles.append(ALL_COLLECTIBLES[collectible_id])

            for user_data in group.user_details:
                user = User(user_data)

                if user.is_clocked_in() and user.id is not logged_in_user.id:
                    clocked_in_users.append({
                        "username": user.username,
                        "clocked_in_at": user.clock_in_timestamp
                    })

                for session in user.sessions:
                    from_time: datetime = session['from_time']
                    to_time: datetime = session['to_time']
                    diff: timedelta = to_time - from_time
                    total_time += diff

            return jsonify({ 
                            "active_users": clocked_in_users, 
                            "total_time_seconds": total_time.total_seconds(),
                            "collectibles": group_collectibles
                            })
        except ValueError as ve:
            abort(400, str(ve))
        except Exception:
            traceback.print_exc()
            abort(500, "Internal Server Error")

    return group_bp
