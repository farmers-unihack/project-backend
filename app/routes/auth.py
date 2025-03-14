from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user_model import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('login', methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = User.find_by_username(username)

    if user == None:
        return jsonify( {"msg": "Invalid username or password"} ), 401

    is_valid = user.is_valid_password(password)

    if not is_valid:
        return jsonify( {"msg": "Invalid username or password"} ), 401

    login_user(user)
    return jsonify({"msg": "logged in"}), 201 

@auth_bp.route('register', methods=['POST'])
def register():
    username = request.form["username"]
    password = request.form["password"]

    user = User.register(username, password)

    if user == None:
        return jsonify({ "msg": "There is already an account registered with that username." }), 400

    return jsonify({ "msg": "Successfully registered the account" }), 200

@auth_bp.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({ "msg": "Successfully logged out" }), 200

@auth_bp.route("/me", methods=['GET'])
@login_required
def me():
    return jsonify(logged_in_as=current_user.username), 200
