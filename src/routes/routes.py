from flask import Blueprint, request
from src.models.database_setup import User, user_schema, users_schema
from src.app import db
main = Blueprint("main", __name__)

@main.route("/")
def index():
    return "hello"
@main.route('/new_user',methods=['POST'])
def create_new_user():
  name = request.json['name']
  email = request.json['email']
  password = request.json['password']

  new_user= User(name, email, password)

  db.session.add(new_user)
  db.session.commit()

  return user_schema.jsonify(new_user)

