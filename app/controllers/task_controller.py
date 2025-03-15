from flask import Blueprint, abort, jsonify, request
from app.repositories.task_repository import TaskRepository

def create_tasks_bp(task_service: TaskRepository) -> Blueprint:
    tasks_bp = Blueprint("tasks", __name__)


    return tasks_bp
