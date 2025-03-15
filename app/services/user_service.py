from datetime import datetime, timedelta
from typing import Optional
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.utils.time import get_current_time


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def find_by_id(self, user_id: str) -> User:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"Not user found with the id {user_id}")
        return user

    def find_by_username(self, username: str) -> User:
        user = self.user_repository.find_by_username(username)
        if not user:
            raise ValueError(f"Not user found with the username {username}")
        return user

    def clock_in_for_user(self, user_id: str, timestamp: datetime) -> None:
        user = self.user_repository.find_by_id(user_id)

        if not user:
            raise ValueError("That user was not found")

        if user.is_clocked_in():
            raise ValueError("User is already clocked in")

        updated = self.user_repository.update_user_by_id(
            user_id, {"$set": {"clock_in_timestamp": timestamp}}
        )
        if not updated:
            raise ValueError("The user was not found to update the field")

    def clock_out_for_user(
        self, user_id: str, keystroke_cnt: Optional[int], mouse_click_cnt: Optional[int]
    ) -> None:
        user = self.user_repository.find_by_id(user_id)

        if not user:
            raise ValueError("That user was not found")

        if not user.is_clocked_in():
            raise ValueError("User is not clocked in")

        from_time = user.clock_in_timestamp
        to_time = get_current_time()
        session = {
            "from_time": from_time,
            "to_time": to_time,
        }
        if keystroke_cnt is not None:
            session["keystroke_cnt"] = keystroke_cnt
        if mouse_click_cnt is not None:
            session["mouse_click_cnt"] = mouse_click_cnt
        update = {"$unset": {"clock_in_timestamp": ""}, "$push": {"sessions": session}}

        updated = self.user_repository.update_user_by_id(user_id, update)
        if not updated:
            raise ValueError("The user was not found to update the field")
