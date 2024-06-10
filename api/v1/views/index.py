#!/usr/bin/python3
"""
index package
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns status"""
    data = {
        "status": "OK"
    }
    response = jsonify(data)
    response.status_code = 200
    return response
