from flask import Blueprint, request, jsonify, make_response
from src.models import User, user_schema, users_schema
from flask_bcrypt import Bcrypt
from ..middleware.utils import token_required, service_connection
from flask import current_app
from src.app import db
import datetime
import jwt
import os

api = Blueprint("main", __name__)
flask_bcrypt = Bcrypt()



@api.route("/")
def index():
    return "Hello"



@api.route('/new_user', methods=['POST'])
@service_connection
def create_new_user():
    '''
    /new_user root will create a new user to the database
    this will recieve the information of the client and collect the information to keep it in th db

    return:
    a json message
    '''
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    user_email = User.query.filter_by(email=email).first()
    user_name = User.query.filter_by(username=username).first()

    if user_email:
        return make_response({"message": "An account with this email already exists. If it's yours, go to login", "error": True}, 409)
    if user_name:
        return make_response({"message": "An account with this username already exists. If it's yours, go to login", "error": True}, 409)

    new_user = User(username=username, email=email, password=flask_bcrypt.generate_password_hash(
        password).decode("utf-8"))

    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify({'message': 'User Created Succesfuly', 'error': False, 'username': new_user.username, 'userID': new_user.public_id}), 201)



@api.route('/authorize', methods=['GET'])
def get_user_token():
    '''
    /validate_user route will validate the user who login and send the current user information in a token

    returns:
    a http response and set the cookies token
    '''
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response({"message":"Please check your login details and try again", "error": True}, 401)

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        user = User.query.filter_by(username=auth.username).first()

    if not user or not flask_bcrypt.check_password_hash(user.password, auth.password):
        return make_response({"message":"Please check your login details and try again", "error": True}, 401)
    if flask_bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=60)}, current_app.config['SECRET_KEY'])
        res = make_response({"message":"User Verification Sucessfuly", "error": False}, 200)
        res.set_cookie("x-access-token", value=token)
        return res

    return make_response({"message":"Please check your login details and try again", "error": True}, 401)


@api.route('/validate')
@token_required
def validate_user_token(current_user):

    user = User.query.filter_by(public_id=current_user.public_id).first()
    if not user:
        return make_response({"Message":"This user does not exist, try again or register"}, 404)

    return make_response({"Message":"User Verification Sucessfuly", "error": False}, 200)

@api.route('/storage/notification', methods=['POST'])
def watch_observer():

    return jsonify(request.json)