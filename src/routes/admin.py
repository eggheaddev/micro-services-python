from flask import Blueprint, request, jsonify, make_response, current_app, redirect, url_for
from flask_bcrypt import Bcrypt
import datetime
import jwt
from src.models import User, Staff
from ..middleware.access_verification import token_required, admin_verificate
from src.app import db

flask_bcrypt = Bcrypt()
admin = Blueprint("admin", __name__)


@admin.route("/db")
@admin_verificate
def get_all_users(res):
    """
    This routes is only for the admins for see all the users register in the database

    params:
    current_user (string): token id for the verification

    return:
    A json with all information of the users
    """

    users = User.query.all()
    staff = Staff.query.all()
    output = []
    staff_output = []
    for user in users:
        user_data = {}
        user_data["public_id"] = user.public_id
        user_data["username"] = user.username
        user_data["email"] = user.email
        user_data["password"] = user.password
        output.append(user_data)

    for admin in staff:
        staff_data = {}
        staff_data["public_id"] = admin.public_id
        staff_data["username"] = admin.username
        staff_data["email"] = admin.email
        staff_data["password"] = admin.password
        staff_output.append(staff_data)

    return jsonify({"users": output, "staff": staff_output}), 200


@admin.route("/staff", methods=["POST"])
def new_staff():
    """
    /staff root will create a new user staff to the database
    this will recieve the information of the client and collect the information to keep it in th db

    return:
    a json message
    """
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]


    if ((staff_email := Staff.query.filter_by(email=email).first()) or
            (user_email := User.query.filter_by(email=email).first())):

        return make_response({"message": "An account with this email already exists. If it's yours, go to login", "error": True }, 409)

    if ((staff_name := Staff.query.filter_by(username=username).first()) or
            (user_name := User.query.filter_by(username=username).first())):

        return make_response({
            "message": "An account with this username already exists. If it's yours, go to login",
            "error": True
            }, 409)

    new_user = Staff(username=username, email=email, password=flask_bcrypt.generate_password_hash(
        password).decode("utf-8"))

    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify({
        "message": "User Created Succesfuly",
        "error": False, "username": new_user.username,
        "userID": new_user.public_id,
        "Admin": new_user.admin}), 201)