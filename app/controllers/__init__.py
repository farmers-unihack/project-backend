from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from pymongo.database import Database

from app.controllers.auth_controller import create_auth_bp
from app.controllers.group_controller import create_group_bp
from app.repositories.group_repository import GroupRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.group_service import GroupService
from app.services.user_service import UserService

def register_controllers(app: Flask, db: Database, bcrypt: Bcrypt, login_manager: LoginManager):
    # Repositories
    user_repository = UserRepository(db)
    group_repository = GroupRepository(db)
    task_repository = TaskRepository(db)

    # Services
    user_service = UserService(user_repository)
    group_service = GroupService(group_repository, user_repository)
    auth_service = AuthService(user_repository, bcrypt)

    # Login manager user loading
    from app.models.user_model import User
    @login_manager.user_loader
    def load_user(user_id):
        return user_repository.find_by_id(user_id)

    # Controllers
    auth_bp = create_auth_bp(auth_service)
    group_bp = create_group_bp(group_service)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(group_bp, url_prefix="/api/group")


