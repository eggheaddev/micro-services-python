from flask import Blueprint, request, jsonify, make_response
from src.models import User, user_schema, users_schema
from ..middleware.utils import token_required
from src.app import db

admin = Blueprint("admin", __name__)


@admin.route("/db")

def get_all_users():
    '''
    This routes is only for the admins for see all the users register in the database

    params:
    current_user (string): token id for the verification

    return:
    A json with all information of the users
    '''
    # if not current_user.admin:
    #     return jsonify({'message': 'Cannot perform that function!'})
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        user_data['storage_id'] = user.storage_id
        output.append(user_data)
    return jsonify({'users': output}), 200


@admin.route('/user-promotion/<public_id>', methods=['PUT'])
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
        return jsonify({'message': 'Cannot perform that function!', "error": True}), 401
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message": 'No user Found', "error": True}), 404
    user.admin = True
    db.session.commit()
    return jsonify({'message': '{} has been promoted'.format(user.username)})
