from datetime import timedelta
from bson.objectid import ObjectId
from app import get_db
from app.models.user_model import UserModel
from app.utils.time import get_current_time


class GroupModel:
    MAX_USERS_IN_GROUP = 6

    @staticmethod
    def create_group(name: str):
        group = {
            "name": name,
            "users": [],
        }
        result = get_db().groups.insert_one(group)
        return result.inserted_id

    @staticmethod
    def get_group(group_id: str):
        try:
            group = get_db().groups.find_one({"_id": ObjectId(group_id)})
            if group is None:
                raise ValueError("Group not found")
            return group
        except ValueError as ve:
            print(f"Error getting group: {ve}")
            return None
        except Exception as e:
            print(f"Unexpected error getting group: {e}")
            return None

    @staticmethod
    def add_user(group_id: str, user_id: str):
        group = GroupModel.get_group(group_id)
        try:
            if len(group["users"]) >= GroupModel.MAX_USERS_IN_GROUP:
                raise ValueError(
                    f"A group can contain a maximum of {GroupModel.MAX_USERS_IN_GROUP} users."
                )
            # check if the user is already in the group
            if user_id in group["users"]:
                raise ValueError("User already in group")
            get_db().groups.update_one(
                {"_id": ObjectId(group_id)}, {"$push": {"users": user_id}}
            )
        except ValueError as ve:
            print(f"Error adding user to group: {ve}")
        except Exception as e:
            print(f"Unexpected error adding user to group {e}")

    @staticmethod
    def remove_user(group_id: str, user_id: str):
        try:
            group = GroupModel.get_group(group_id)
            if group is None:
                raise ValueError("Group not found")

            get_db().groups.update_one(
                {"_id": ObjectId(group_id)}, {"$pull": {"users": user_id}}
            )

            # Check if the group is empty after removing the user, if so, delete the group
            group = GroupModel.get_group(group_id)
            if group and not group["users"]:
                get_db().groups.delete_one({"_id": ObjectId(group_id)})

        except ValueError as ve:
            print(f"Error removing user from group: {ve}")
        except Exception as e:
            print(f"Unexpected error removing user from group: {e}")

    @staticmethod
    def get_completed_tasks(group_id: str, time_limit: timedelta):
        """
        Get all the tasks completed by the users in the group within the time limit (e.g. last 24 hours)
        """
        group = GroupModel.get_group(group_id)
        if group is None:
            return None

        # Get all the users in the group and their completed tasks
        user_model = UserModel()
        users = filter(
            lambda user: user is not None,
            map(lambda user_id: user_model.get_user(user_id), group["users"]),
        )
        # Get all the tasks completed by the users in the group
        tasks = []
        for user in users:
            tasks.extend(
                filter(
                    map(lambda user: user["tasks"], users),
                    lambda task: task["completed"]
                    and get_current_time() - task["completion_date"] > time_limit,
                )
            )
        return list(tasks)
