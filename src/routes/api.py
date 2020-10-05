from flask import Blueprint, request, jsonify, make_response, current_app
from flask_bcrypt import Bcrypt
from flask_cors import cross_origin
import requests
import datetime
import jwt
import os
from ..middleware.access_verification import token_required
from src.models import User, Staff
from src.app import db

api = Blueprint("main", __name__)
flask_bcrypt = Bcrypt()



@api.route("/")
@cross_origin()
def index():
    response = jsonify({"message": "I'm Awake"})
    return  response


@api.route("/new_user", methods=["POST"])
@cross_origin()
def create_new_user():
    """
    /new_user root will create a new user to the database
    this will recieve the information of the client and collect the information to keep it in th db

    return:
    a json message
    """
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    user_email = User.query.filter_by(email=email).first()
    user_name = User.query.filter_by(username=username).first()
    staff_email = Staff.query.filter_by(email=email).first()
    staff_name = Staff.query.filter_by(username=username).first()

    if user_email or staff_email:

        return make_response({
            "message": "An account with this email already exists. If it's yours, go to login",
            "error": True}, 409)

    if user_name or staff_name:

        return make_response({
            "message": "An account with this username already exists. If it's yours, go to login",
            "error": True}, 409)

    new_user = User(username=username, email=email, password=flask_bcrypt.generate_password_hash(
        password).decode("utf-8"))

    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify({
        "message": "User Created Succesfuly",
        "error": False, 
        "username": new_user.username, 
        "userID": new_user.public_id}), 201)


@api.route("/authorize", methods=["POST"])
@cross_origin()
def get_user_token():
    """
    /authorize route will validate the user who login and send the current user information in a token

    returns:
    a http response and set the cookies token
    """

    username = request.json["username"]
    password = request.json["password"]
    if not username or not password:

        return make_response({
            "message": "Please check your login details and try again",
            "error": True}, 401)

    user = User.query.filter_by(email=username).first()

    if not user:
        user = User.query.filter_by(username=username).first()

        if not user:
            return make_response({
                "message": "This user does not exists, please go and register",
                "error": True
            }, 404)

        elif not flask_bcrypt.check_password_hash(user.password, password):
            return make_response({
                "message": "Please check your login details and try again",
                "error": True}, 401)

    if flask_bcrypt.check_password_hash(user.password, password):
        #toke is available for 7 days
        token = jwt.encode({
            "public_id": user.public_id,
            "username": user.username,
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(minutes=10080)}, current_app.config["SECRET_KEY"])

        res = make_response({
            "message": "User Verification Sucessfuly",
            "error": False,
            "x-access-token": str(token)[(str(token).index("'") + 1) : str(token).index("'", 2)]
            }, 200)
        res.set_cookie("x-access-token", value=token, samesite='Lax', secure=True)

        return res

    return make_response({
        "message": "Please check your login details and try again",
        "error": True}, 401)

@api.route("/validate", methods=["POST"])
@token_required
def validate_user_token(current_user):

    """
    validate the token if the user exists

    params: current_user (user token)

    return: A response 200 or 404
    """
    user = User.query.filter_by(public_id=current_user.public_id).first()
    if not user:
        return make_response({
            "message":"This user does not exist, try again or register",
            "error": True  }, 404)


    return make_response({
        "message":"User Verification Sucessfuly",
        "error": False,
        "username": user.username}, 200)
