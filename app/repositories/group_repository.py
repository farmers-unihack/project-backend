from typing import Optional
from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import UpdateResult

from app.models.group_model import Group

class GroupRepository():
    def __init__(self, db: Database) -> None:
        self.db = db

    def create_group(self, name: str) -> Optional[Group]:
        group_data = {
            "name": name,
            "users": [],
        }

        result = self.db.groups.insert_one(group_data)

        if not result.inserted_id:
            return None

        group_data["_id"] = result.inserted_id
        return Group(group_data) 

    def find_group_by_id(self, group_id: str) -> Optional[Group]:
        group_data = self.db.groups.find_one({"_id": ObjectId(group_id)})
        return Group(group_data) if group_data else None 

    def add_user_to_group(self, group_id: str, user_id: str) -> UpdateResult:
        return self.db.groups.update_one( {"_id": ObjectId(group_id)}, {"$push": { "users": user_id }} )

    def remove_user_from_group(self, group_id: str, user_id: str) -> UpdateResult:
        return self.db.groups.update_one( {"_id": ObjectId(group_id)}, {"$pull": { "users": user_id }} )
