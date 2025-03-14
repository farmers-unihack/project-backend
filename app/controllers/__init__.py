from flask_bcrypt import Bcrypt
from pymongo.database import Database

from app.repositories.group_repository import GroupRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.group_service import GroupService
from app.services.user_service import UserService

def register_controllers(db: Database, bcrypt: Bcrypt):
    # Repositories
    user_repository = UserRepository(db)
    group_repository = GroupRepository(db)
    task_repository = TaskRepository(db)

    # Services
    user_service = UserService(user_repository)
    group_service = GroupService(group_repository)
    auth_service = AuthService(user_repository, bcrypt)

    # Controllers

