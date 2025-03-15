from typing import Any
import string
import secrets


class Group:
    MAX_USERS_IN_GROUP = 4

    def __init__(self, data: Any) -> None:
        self.id = data["_id"]
        self.name = data["name"]
        self.users = data["users"]
        self.user_details = data["user_details"]
        self.invite_code = data["invite_code"]

    def get_member_count(self):
        return len(self.users)

    def contains_user(self, user_id: str):
        return user_id in self.users

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "users": self.users,
            "user_details": self.user_details,
            "invite_code": self.invite_code,
        }

    @staticmethod
    def generate_unique_invite_code(id, length=6):
        """Generates a unique code based on the group id"""
        alphabet = string.ascii_letters + string.digits
        seed = str(id) + secrets.token_hex(8)
        random_generator = secrets.SystemRandom(seed.encode())
        code = "".join(random_generator.choice(alphabet) for _ in range(length))
        return code
