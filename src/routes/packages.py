from flask import Blueprint, jsonify, make_response, request, current_app
import requests

storage = Blueprint("storage", __name__)


@storage.route('/notification', methods=['POST'])
def watch_observer():

    return jsonify(request.json)


@storage.route('/packages', methods=['GET'])
def get_all_packages():

    ses = requests.session()
    req = ses.get('http://localhost:3000/packages')
    pkg_info = req.json()

    return make_response(jsonify(pkg_info), 200)

@storage.route('/package/<id>', methods=['GET'])
def get_one_package(id):

    token = current_app.config['ACCESS_TOKEN']
    headers = {"access_token": token}
    ses = requests.session()
    req = ses.get(f'http://localhost:3000/package/{id}', headers=headers)
    pkg_info = req.json()

    return make_response(jsonify(pkg_info), 200)
