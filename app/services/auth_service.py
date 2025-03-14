from typing import Optional
from flask_bcrypt import Bcrypt
from app.models.user_model import User
from app.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self, user_repository: UserRepository, bcrypt: Bcrypt) -> None:
        self.user_repository = user_repository
        self.bcrypt = bcrypt

    def login(self, username: str, password: str) -> Optional[User]:
        user = self.user_repository.find_by_username(username)

        if not user:
            return None

        if not self.validate_password(user, password):
            return None

        return user

    def register(self, username: str, password: str) -> Optional[User]:
        if self.user_repository.find_by_username(username):
            return None
        hashed_password = self.bcrypt.generate_password_hash(password).decode("utf-8")
        self.user_repository.create_user(username, hashed_password)

    def validate_password(self, user: User, expected_pass: str) -> bool:
        return self.bcrypt.check_password_hash(user.hashed_password, expected_pass)
