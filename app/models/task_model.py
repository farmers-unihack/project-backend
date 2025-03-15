from datetime import timedelta
from app.utils.time import get_current_time


class Task:
    def __init__(self, data):
        self.id = data["_id"]
        self.name = data["name"]
        self.description = data["description"]
        self.completion_date = data["completion_date"]
        self.completed = data["completed"]

    def is_completed_within_recent_time(self, time_limit: timedelta):
        return self.completed and get_current_time() - self.completion_date < time_limit
