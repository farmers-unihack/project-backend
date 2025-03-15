from typing import Optional
from pymongo.database import Database
from bson import ObjectId

from app.models.user_model import User


class UserRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def find_by_id(self, user_id: str) -> Optional[User]:
        data = self.db.users.find_one({"_id": ObjectId(user_id)})
        return User(data) if data else None

    def find_by_username(self, username: str) -> Optional[User]:
        data = self.db.users.find_one({"username": username})
        return User(data) if data else None

    def update_user_by_id(self, user_id: str, update_fields: dict) -> bool:
        result = self.db.users.update_one(
            {"_id": ObjectId(user_id)}, update_fields
        )

        return result.modified_count > 0

    def create_user(self, username: str, hashed_password: str) -> bool:
        if self.find_by_username(username):
            return False 

        user = {
            "username": username,
            "hashed_password": hashed_password,
        }

        result = self.db.users.insert_one(user)

        if result.inserted_id == None:
            return False 

        return True

        result = self.db.users.insert_one(user_data)
        if result.inserted_id is None:
            return None
        user_data["_id"] = result.inserted_id
        return User(user_data)
