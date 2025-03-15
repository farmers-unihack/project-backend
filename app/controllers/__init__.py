from flask import Flask
from flask_bcrypt import Bcrypt
from pymongo.database import Database

from app.controllers.auth_controller import create_auth_bp
from app.controllers.group_controller import create_group_bp
from app.controllers.task_controller import create_task_bp
from app.repositories.group_repository import GroupRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.group_service import GroupService
from app.services.task_service import TaskService
from app.services.user_service import UserService


def register_controllers(app: Flask, db: Database, bcrypt: Bcrypt):
    # Repositories
    user_repository = UserRepository(db)
    group_repository = GroupRepository(db)
    task_repository = TaskRepository(db)

    # Services
    group_service = GroupService(group_repository, user_repository, task_repository)
    auth_service = AuthService(app, user_repository, bcrypt)
    task_service = TaskService(task_repository, user_repository)

    # Controllers
    auth_bp = create_auth_bp(auth_service)
    group_bp = create_group_bp(group_service)
    task_bp = create_task_bp(task_service, auth_service)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(group_bp, url_prefix="/api/group")
    app.register_blueprint(task_bp, url_prefix="/api/task")
