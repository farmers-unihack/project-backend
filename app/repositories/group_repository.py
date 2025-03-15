from typing import Optional
from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import UpdateResult
from pymongo.results import DeleteResult

from app.models.group_model import Group


class GroupRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create_group(self, name: str, user_id: str) -> bool:
        group_data = {
            "name": name,
            "users": [ObjectId(user_id)],
            "collectibles": [],
            "invite_code": Group.generate_unique_invite_code(user_id),
        }

        # FIXME: Conflict resolution?

        result = self.db.groups.insert_one(group_data)

        if not result.inserted_id:
            return False

        return True

    def find_group_by_invite_code(self, invite_code: str) -> Optional[str]:
        group_data = self.db.groups.find_one({"invite_code": invite_code})
        return group_data["_id"] if group_data else None

    def find_group_by_id(self, group_id: str) -> Optional[Group]:
        group_data = self.db.groups.aggregate(
            [
                {"$match": {"_id": ObjectId(group_id)}},
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "users",
                        "foreignField": "_id",
                        "as": "user_details",
                    }
                },
                {"$project": {"user_details.hashed_password": 0}},
                {"$limit": 1},
            ]
        )
        group_data = next(group_data, None)

        return Group(group_data) if group_data else None

    def find_group_by_user_id(self, user_id: str) -> Optional[Group]:
        group_data = self.db.groups.aggregate(
            [
                {"$match": {"users": {"$in": [ObjectId(user_id)]}}},
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "users",
                        "foreignField": "_id",
                        "as": "user_details",
                    }
                },
                {"$project": {"user_details.hashed_password": 0}},
                {"$limit": 1},
            ]
        )
        group_data = next(group_data, None)
        return Group(group_data) if group_data else None

    def add_user_to_group(self, group_id: str, user_id: str) -> UpdateResult:
        return self.db.groups.update_one(
            {"_id": ObjectId(group_id)}, {"$push": {"users": ObjectId(user_id)}}
        )

    def remove_user_from_group(self, group_id: str, user_id: str) -> UpdateResult:
        return self.db.groups.update_one(
            {"_id": ObjectId(group_id)}, {"$pull": {"users": ObjectId(user_id)}}
        )

    def add_collectible_to_group(
        self, group_id: str, collectible_name: str
    ) -> UpdateResult:
        return self.db.groups.update_one(
            {"_id": ObjectId(group_id)}, {"$push": {"collectibles": collectible_name}}
        )

    def delete_group_by_id(self, group_id: str) -> DeleteResult:
        return self.db.groups.delete_one({"_id": ObjectId(group_id)})
