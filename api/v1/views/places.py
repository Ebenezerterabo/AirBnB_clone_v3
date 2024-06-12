#!/usr/bin/python3
"""
Place view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects
    """
    city = storage.get(City, city_id)
    if city:
        place_list = []
        for place in city.places:
            place_list.append(place.to_dict())
        return jsonify(place_list)
    else:
        return abort(404)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a place object
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        return abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(place_id):
    """
    Deletes a Place object
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """
    Creates a Place object
    """
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    elif not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif 'user_id' not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    elif 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    new_place = Place(**request.get_json())
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """
    Updates a Place object
    """
    place = storage.get(Place, user_id)
    if not place:
        return abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    else:
        for key, value in request.get_json().items():
            if key not in ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
