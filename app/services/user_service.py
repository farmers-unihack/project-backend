from app.models.user_model import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def find_by_id(self, user_id: str) -> User:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"Not user found with the id {user_id}")
        return user

    def find_by_username(self, username: str) -> User:
        user = self.user_repository.find_by_username(username)
        if not user:
            raise ValueError(f"Not user found with the username {username}")
        return user
