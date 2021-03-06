from flask import Blueprint, jsonify, make_response, request, current_app
from flask_cors import cross_origin
import requests
storage = Blueprint("storage", __name__)

@storage.route("/notification", methods=["POST"])
@cross_origin()
def watch_observer():

    return jsonify(request.json)


@storage.route("/packages", methods=["GET"])
@cross_origin()
def get_all_packages():

    token = current_app.config["ACCESS_TOKEN"]
    headers = {"access_token": token}
    ses = requests.session()
    req = ses.get("https://storage-hostify-service.herokuapp.com/api/packages", headers=headers)
    pkg_info = req.json()

    return make_response(pkg_info, 200)

@storage.route("/package", methods=["POST"])
@cross_origin()
def get_one_package():

    package_name = request.json['name']
    token = current_app.config["ACCESS_TOKEN"]
    headers = {"access_token": token}
    ses = requests.session()
    req = ses.get(f"https://storage-hostify-service.herokuapp.com/api/package", headers=headers, json={"name":package_name})
    pkg_info = req.json()

    return make_response(jsonify(pkg_info), 200)
