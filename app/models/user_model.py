from typing import Any, Optional
from flask_login import UserMixin
from bson import ObjectId

from app.extensions import get_db, bcrypt

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data["_id"]
        self.username = user_data["username"] 
        self.hashed_password = user_data["hashed_password"] 

    def is_valid_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.hashed_password, password)

    @staticmethod
    def find_by_id(user_id):
        user_data = get_db().users.find_one({ "_id": ObjectId(user_id) })
        return User(user_data) if user_data else None

    @staticmethod
    def find_by_username(username: str) -> Optional[Any]:
        user_data = get_db().users.find_one({ "username": username })
        return User(user_data) if user_data else None

    @staticmethod
    def register(username: str, password: str) -> Optional[Any]:
        if User.find_by_username(username):
            return None

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        result = get_db().users.insert_one({
            "username": username,
            "hashed_password": password_hash,
        })

        return User({ "_id": result.inserted_id, "username": username, "hashed_password": password_hash }) 
