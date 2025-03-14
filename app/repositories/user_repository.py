from typing import Optional
from pymongo.database import Database
from bson import ObjectId

from app.models.user_model import User

class UserRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def find_by_id(self, user_id) -> Optional[User]:
        user_data = self.db.users.find_one({ "_id": ObjectId(user_id) })
        return User(user_data) if user_data else None

    def find_by_username(self, username: str) -> Optional[User]:
        user_data = self.db.users.find_one({ "username": username })
        return User(user_data) if user_data else None

    def create_user(self, username: str, hashed_password: str) -> Optional[User]:
        if self.find_by_username(username):
            return None

        result = self.db.users.insert_one({
            "username": username,
            "hashed_password": hashed_password,
        })

        return User({ "_id": result.inserted_id, "username": username, "hashed_password": hashed_password }) 

