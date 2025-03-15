
class User():
    def __init__(self, user_data: dict):
        self.id = str(user_data["_id"])
        self.username = user_data["username"] 
        self.hashed_password = user_data["hashed_password"] 
        self.clock_in_timestamp = user_data.get("clock_in_timestamp", None)

    def is_clocked_in(self) -> bool:
        return not (self.clock_in_timestamp == None)
