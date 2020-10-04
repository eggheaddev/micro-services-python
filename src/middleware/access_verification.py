from flask import request, jsonify, current_app, Response, make_response
from functools import wraps
from flask_bcrypt import Bcrypt
import datetime
import requests
import socket
import jwt
from src.models import User, Staff



flask_bcrypt = Bcrypt()

# Decorator to protetec our routes for non-register users
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({
                "message": "Token is missing!",
                "error": True
                }), 403

        try:

            data = jwt.decode(token, current_app.config["SECRET_KEY"])
            current_user = User.query.filter_by(
                public_id=data["public_id"]).first()

        except:

            return jsonify({
                "message": "Token is invalid!",
                "error": True
                }), 403

        return f(current_user, *args, **kwargs)

    return decorated


def admin_verificate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response({
                "message": "You are not an administrator or your details are not correct, please check your login details and try again", 
                "error": True}, 401)

        user_admin = Staff.query.filter_by(email=auth.username).first()

        if not user_admin:
            user_admin = Staff.query.filter_by(username=auth.username).first()

            if not user_admin or not flask_bcrypt.check_password_hash(user_admin.password, auth.password):

                return make_response({
                    "message": "You are not an administrator or your details are not correct, please check your login details and try again",
                    "error": True}, 401)

        if flask_bcrypt.check_password_hash(user_admin.password, auth.password):

            res = make_response({"message": "User Verification Sucessfuly", "error": False}, 200)
            return f(res, *args, **kwargs)

    return decorated


def create_micro_service_connection():
    url = "http://localhost:3000/connect"
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    ses = requests.session()
    response = ses.post(url, data={
        "ip": ip_address,
        "ServiceName": hostname,
        "description": "test backend service"
    })
    for cookie in cookieJar:
        print(cookie)
    print(response.text)
