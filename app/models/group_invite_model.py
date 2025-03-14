from bson.objectid import ObjectId
from app.models.group_model import GroupModel
from app.models.user_model import User
from app.extensions import get_db


class GroupInviteModel:
    MAX_USERS_IN_GROUP = 6

    @staticmethod
    def create_group_invite(group_id: str, user_id: str):
        # check if a user exists and group exists
        group = GroupModel.get_group(group_id)
        user = User.find_by_id(user_id)

        if group == None:
            raise ValueError("Specfied group id was not found")

        if user_id in group["users"]:
            raise ValueError("User is already in the group")

        invite = {
            "group_id": group_id,
            "user_id": None,
        }

        result = get_db().insert_one(invite)
        return result.inserted_id

    @staticmethod
    def accept_group_invite(invite_id: str):
        invite = get_db().find_one({"_id": ObjectId(invite_id)})
        group_id = invite["group_id"]
        user_id = invite["user_id"]

        group_model = GroupModel()

        group_model.add_user(user_id, group_id)
        get_db().delete_one({"_id": ObjectId(invite_id)})

    @staticmethod
    def reject_group_invite(invite_id: str):
        get_db().delete_one({"_id": ObjectId(invite_id)})
