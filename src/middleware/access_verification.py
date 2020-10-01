from flask import request, jsonify, current_app, Response
from functools import wraps
from src.models import User, db
import requests
import socket
import jwt

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


def service_connection(f, url):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = current_app.config["ACCESS_TOKEN"]
        ses = requests.session()
        headers = {"access_token": token}

        resp = ses.get(url, headers = headers)
        return resp.json()
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
