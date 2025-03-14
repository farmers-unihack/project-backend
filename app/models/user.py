from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username: str, hashed_password: str):
        self.username = username
        self.hashed_password = hashed_password


