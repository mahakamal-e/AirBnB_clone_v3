#!/usr/bin/python3
""" User route that handles all default RESTFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET'])
def get_users():
    """ List all users """
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]

    return jsonify(users_list), 200


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ Retrieves a user by id """
    user = storage.get(User, user_id)
    if user is None:
        response = jsonify({"error": "Not found"})
        response.status_code = 404
        return response
    return jsonify(user.to_dict()), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    """ Creates a new user """
    user_data = request.get_json()

    if user_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if not user_data.get('email'):
        return jsonify({"error": "Missing email"}), 400
    if not user_data.get('password'):
        return jsonify({"error": "Missing password"}), 400

    new_user = User(**user_data)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes a user by id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ Update a user by user_id """
    current_user = storage.get(User, user_id)
    if current_user is None:
        abort(404)
    user_data = request.get_json()
    if user_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    updated_data = ['first_name', 'last_name', 'email', 'password']
    for data in updated_data:
        setattr(current_user, data,
                user_data.get(data, getattr(current_user, data)))
    storage.save()
    return jsonify(current_user.to_dict()), 200
