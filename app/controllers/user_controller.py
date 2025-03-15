from flask import Blueprint
from app.services.user_service import UserService

def create_user_bp(user_service: UserService) -> Blueprint:
    user_bp = Blueprint("user", __name__)

    @user_bp.route("/clockin", methods=["POST"])
    def clock_in():


    return user_bp 
