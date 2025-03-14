from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data["_id"]
        self.username = user_data["username"] 
        self.hashed_password = user_data["hashed_password"] 
