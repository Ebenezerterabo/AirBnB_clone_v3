#!/usr/bin/python3
"""
State view
"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all city objects of a state
    """
    state = storage.get(State, state_id)
    if state:
        cities = state.cities
        city_list = [city.to_dict() for city in cities]
        return jsonify(city_list)
    else:
        return abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        return abort(404)


@app_views.route('cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """
    Creates a city object
    """
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        else:
            if 'name' in request.get_json():
                new_city = City(**request.get_json())
                new_city.state_id = state_id
                storage.new(new_city)
                storage.save()
                return jsonify(new_city.to_dict()), 201
            else:
                return jsonify({"error": "Missing name"}), 400
    else:
        return abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """
    update a city object
    """
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        else:
            for key, value in request.get_json().items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(city, key, value)
            storage.save()
            return jsonify(city.to_dict()), 200
    else:
        return abort(404)
