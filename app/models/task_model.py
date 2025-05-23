from datetime import timedelta
import datetime
from app.utils.time import get_current_time


class Task:
    def __init__(self, data):
        self.id = data["_id"]
        self.name = data["name"]
        self.description = data["description"]
        self.completion_date = data["completion_date"]
        self.completed = data["completed"]
        self.user_id = data["user_id"]

    def is_completed_within_recent_time(self, time_limit: timedelta):
        return (
            self.completed
            and get_current_time() - self.completion_date.replace(tzinfo=datetime.UTC)
            < time_limit
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "completion_date": self.completion_date,
            "completed": self.completed,
            "user_id": self.user_id,
        }