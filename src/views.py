from flask import Blueprint, request, jsonify, make_response
from .models import User, user_schema, users_schema
from flask_bcrypt import Bcrypt
from .utils import token_required
from flask import current_app
from .app import db
import datetime
import jwt
import os

main = Blueprint("main", __name__)
flask_bcrypt = Bcrypt()


@main.route("/")
def index():
    return " "


@main.route("/admin-db")
@token_required
def get_all_users(current_user):
    '''
    This routes is only for the admins for see all the users register in the database

    params:
    current_user (string): token id for the verification

    return:
    A json with all information of the users
    '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'users': output}), 200


@main.route('/new_user', methods=['POST'])
def create_new_user():
    '''
    /new_user root will create a new user to the database
    this will recieve the information of the client and collect the information to keep it in th db

    return:
    a json message
    '''
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()

    if user:
        return make_response("An account with this email already exists. If it's yours, go to login", 409)

    new_user = User(name=name, email=email, password=flask_bcrypt.generate_password_hash(
        password).decode("utf-8"))

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'Message': 'User Created Succesfuly'})

@main.route('/user-promotion/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    '''
    /user-promotion/<public-id route will promote an user to admin
    only an admin can use this route for promote another user

    params:
    current_id (String): token of the user admin
    public_id (string): user's id who will be promote
    '''
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message": 'No user Found'})
    user.admin = True
    db.session.commit()
    return jsonify({'message': '{} has been promoted'.format(user.name)})


@main.route('/validate_user', methods=['GET'])
def validate_user():
    '''
    /validate_user route will validate the user who login and send the current user information in a token 

    returns:
    a http response and set the cookies token
    '''
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response("Please check your login details and try again", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=auth.username).first()

    if not user or not flask_bcrypt.check_password_hash(user.password, auth.password):
        return make_response("Please check your login details and try again", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if flask_bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
        res = make_response("User Verification Sucessfuly", 200)
        res.set_cookie("x-access-token", value= token)
        return res

    return make_response("Please check your login details and try again", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
