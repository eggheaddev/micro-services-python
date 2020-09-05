from flask import Blueprint, request
from src.models.database_setup import User, user_schema, users_schema
from src.app import db
from flask_bcrypt import Bcrypt


main = Blueprint("main", __name__)
flask_bcrypt = Bcrypt()


@main.route("/")
def index():
    return "hello"
@main.route('/new_user',methods=['POST'])
def create_new_user():
  name = request.json['name']
  email = request.json['email']
  password = request.json['password']

  new_user= User(name, email, password=flask_bcrypt.generate_password_hash(password).decode("utf-8"))

  db.session.add(new_user)
  db.session.commit()

  return user_schema.jsonify(new_user)