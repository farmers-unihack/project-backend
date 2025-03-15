

class User():
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"] 
        self.hashed_password = user_data["hashed_password"] 
