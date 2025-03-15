from typing import Any


class Group:
    MAX_USERS_IN_GROUP = 4

    def __init__(self, data: Any) -> None:
        self.id = data["_id"]
        self.name = data["name"]
        self.users = data["users"]
        self.user_details = data["user_details"]
        self.collectibles = data["collectibles"]

    def get_member_count(self):
        return len(self.users)

    def contains_user(self, user_id: str):
        return user_id in self.users
