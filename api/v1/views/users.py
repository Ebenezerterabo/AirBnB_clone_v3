#!/usr/bin/python3
"""
Amenity view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects
    """
    user_list = []
    for user in storage.all(User).values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        return abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a User object
    """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    elif 'password' not in request.get_json():
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**request.get_json())
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """
    Updates a User object
    """
    user = storage.get(User, user_id)
    if not user:
        return abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    else:
        for key, value in request.get_json().items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
