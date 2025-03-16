from datetime import datetime, timedelta, timezone
from functools import wraps
import traceback
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from app.exceptions.auth_exception import AuthException
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
import jwt


class AuthService:
    def __init__(self, app: Flask, user_repository: UserRepository, bcrypt: Bcrypt) -> None:
        self.app = app
        self.user_repository = user_repository
        self.bcrypt = bcrypt

    def login(self, username: str, password: str) -> tuple[User, str]:
        user = self.user_repository.find_by_username(username)

        if not user:
            raise AuthException("The user did not provide a valid username")

        if not self.validate_password(user, password):
           raise AuthException("The user did not provide a valid password") 

        token = jwt.encode({        
                            'user_id': str(user.id),
                            'username': user.username,
                            'exp' : datetime.now(timezone.utc) + timedelta(days = 7)
                            }, self.app.config["SECRET_KEY"])

        return user, token

    def register(self, username: str, password: str) -> None:
        if self.user_repository.find_by_username(username):
            raise AuthException(f"A user with the name {username} already exists") 
        hashed_password = self.bcrypt.generate_password_hash(password).decode("utf-8")
        if not self.user_repository.create_user(username, hashed_password):
            raise AuthException(f"A failuer occured while creating a new user") 

    def validate_password(self, user: User, expected_pass: str) -> bool:
        return self.bcrypt.check_password_hash(user.hashed_password, expected_pass)

    def protect_with_jwt(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                return jsonify({'message' : 'Token is missing !!'}), 401
      
            try:
                data = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = self.user_repository.find_by_id(data['user_id'])
                if not current_user:
                    return jsonify({
                        'message' : 'Token is invalid !!'
                    }), 401
            except:
                traceback.print_exc()
                return jsonify({
                    'message' : 'Token is invalid !!'
                }), 401

            return  f(current_user, *args, **kwargs)
  
        return decorated
