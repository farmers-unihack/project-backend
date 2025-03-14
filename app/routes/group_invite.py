from flask import Blueprint, abort, jsonify, request

from app.models.group_invite_model import GroupInviteModel

group_invite_bp = Blueprint("group_invite", __name__)


@group_invite_bp.route("/", methods=["POST"])
def invite():
    try:
        user_id = request.json["user_id"]
        group_id = request.json["group_id"]
        GroupInviteModel.create_group_invite(user_id, group_id)
        return jsonify({"msg": "Invited user successfully"}), 201
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        print(e)
        abort(500, "Internal Server Error")


@group_invite_bp.route("accept", methods=["POST"])
def accept():
    try:
        user_id = request.json["user_id"]
        group_id = request.json["group_id"]
        GroupInviteModel.accept_group_invite(user_id, group_id)
        return jsonify({"msg": "Accepted group invite successfully"}), 200
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, "Internal Server Error")


@group_invite_bp.route("reject", methods=["POST"])
def reject():
    try:
        user_id = request.json["user_id"]
        group_id = request.json["group_id"]
        GroupInviteModel.reject_group_invite(user_id, group_id)
        return jsonify({"msg": "Rejected group invite successfully"}), 200
    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        abort(500, "Internal Server Error")
