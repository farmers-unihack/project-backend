from flask import Blueprint, abort, jsonify, request
from app.services.group_service import GroupService

def create_tasks_bp(task_service: Task) -> Blueprint:
    group_bp = Blueprint("group", __name__)
