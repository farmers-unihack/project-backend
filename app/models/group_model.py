from bson.objectid import ObjectId
from app import get_db
from pymongo.collection import Collection


class GroupModel:
    MAX_USERS_IN_GROUP = 6

    def __init__(self):
        self.collection: Collection = get_db().groups

    def create_group(self, name):
        group = {
            "name": name,
            "users": [],
        }
        result = self.collection.insert_one(group)
        return result.inserted_id

    def get_group(self, group_id):
        try:
            group = self.collection.find_one({"_id": ObjectId(group_id)})
            if group is None:
                raise ValueError("Group not found")
            return group
        except ValueError as ve:
            print(f"Error getting group: {ve}")
            return None
        except Exception as e:
            print(f"Unexpected error getting group: {e}")
            return None

    def add_user(self, group_id, user_id):
        group = self.get_group(group_id)
        if len(group["users"]) >= self.MAX_USERS_IN_GROUP:
            raise ValueError(
                f"A group can contain a maximum of {self.MAX_USERS_IN_GROUP} users."
            )

        try:
            self.collection.update_one(
                {"_id": ObjectId(group_id)}, {"$push": {"users": user_id}}
            )
        except ValueError as ve:
            print(f"Error adding user to group: {ve}")
        except Exception as e:
            print(f"Unexpected error adding user to group {e}")

    def remove_user(self, group_id, user_id):
        try:
            group = self.get_group(group_id)
            if group is None:
                raise ValueError("Group not found")
    
            self.collection.update_one(
                {"_id": ObjectId(group_id)}, {"$pull": {"users": user_id}}
            )
    
            # Check if the group is empty after removing the user, if so, delete the group
            group = self.get_group(group_id)
            if group and not group["users"]:
                self.collection.delete_one({"_id": ObjectId(group_id)})
    
        except ValueError as ve:
            print(f"Error removing user from group: {ve}")
        except Exception as e:
            print(f"Unexpected error removing user from group: {e}")
