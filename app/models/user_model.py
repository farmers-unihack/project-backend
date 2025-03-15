import datetime


class User:
    def __init__(self, user_data: dict):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]
        self.hashed_password = user_data.get("hashed_password", None)
        self.clock_in_timestamp = user_data.get("clock_in_timestamp", None)
        self.sessions: list[dict[str, datetime.datetime]] = user_data.get(
            "sessions", []
        )

    def is_clocked_in(self) -> bool:
        return self.clock_in_timestamp is not None

    def get_total_session_time(self) -> int:
        return sum(
            [
                (session["to_time"] - session["from_time"]).seconds
                for session in self.sessions
            ]
        )
