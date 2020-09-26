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

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({
                'message': 'Token is missing!',
                'error': True
                }), 403

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except:
            return jsonify({
                'message': 'Token is invalid!',
                'error': True
                }), 403

        return f(current_user, *args, **kwargs)

    return decorated


def service_connection(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = current_app.config['ACCESS_TOKEN']
        ses = requests.session()
        headers = {"access_token": token}
        user_info = f(**kwargs)
        resp = ses.post('http://127.0.0.1:3000/api/test', json={
            "user": str(user_info.json["username"]),
            "public_id": str(user_info.json["userID"])
        })
        user = User.query.filter_by(public_id=user_info.json['userID']).first()
        user.storage_id = str(resp.json())
        db.session.commit()
        print(user_info.json)
        return user_info
    return decorated



def create_micro_service_connection():
    url = 'http://localhost:3000/connect'
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    ses = requests.session()
    response = ses.post(url, data={
        "ip": ip_address,
        "ServiceName": "backend test",
        "description": "test backend service"
    })
    f = open('.env', 'a')
    f.write("access_token='{}'".format(ses.cookies['access_token']))
    f.close()
    cookieJar = ses.cookies
    for cookie in cookieJar:
        print(cookie)
    print(response.text)
