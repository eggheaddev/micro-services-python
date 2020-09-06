from flask import Blueprint, request, jsonify, make_response
from .models import User, user_schema, users_schema
from flask_bcrypt import Bcrypt
from functools import wraps
from .app import db
import datetime
import jwt
import os

main = Blueprint("main", __name__)
flask_bcrypt = Bcrypt()

# Decorator to protetec our routes for non-register users


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, os.environ.get('SECRET_KEY'))
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

#This routes is only for the admins for see all the users register in the database
@main.route("/")
@token_required
def get_all_users(current_user):
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
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    new_user = User(name=name, email=email, password=flask_bcrypt.generate_password_hash(
        password).decode("utf-8"))

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'Message': 'User Created Succesfuly'})

@main.route('/user/<public_id>', methods=['GET'])
def promote_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message": 'No user Found'})
    user.admin = True
    db.session.commit()
    return jsonify({'message': '{} has been promoted'.format(user.name)})


@main.route('/validate_user', methods=['GET'])
def validate_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response("Please check your login details and try again", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()

    if not user or not flask_bcrypt.check_password_hash(user.password, password):
        return make_response("Please check your login details and try again", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if flask_bcrypt.check_password_hash(user.password, password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, os.environ.get('SECRET_KEY'))
        res = make_response("User Verification Sucessfuly", 200)
        res.set_cookie("x-access-token", value= token)
        return res

    return make_response("Please check your login details and try again", 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
