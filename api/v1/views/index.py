#!/usr/bin/python3
"""
index package
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns status"""
    data = {
        "status": "OK"
    }
    response = jsonify(data)
    response.status_code = 200
    return response


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """returns stats"""
    stats = {}
    stats['amenities'] = storage.count("Amenity")
    stats['cities'] = storage.count("City")
    stats['places'] = storage.count("Place")
    stats['reviews'] = storage.count("Review")
    stats['states'] = storage.count("State")
    stats['users'] = storage.count("User")
    return jsonify(stats)
