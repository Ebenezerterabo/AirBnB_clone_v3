#!/usr/bin/python3
"""
Place view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects
    """
    place = storage.get(Place, place_id)
    if place:
        review_list = []
        for review in place.reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)
    else:
        return abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a review object
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        return abort(404)


@app_views.route('/review/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(review_id):
    """
    Deletes a review object
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_place(place_id):
    """
    Creates a Review object
    """
    place = storage.get(Place, place_id)
    user = storage.get(User, request.get_json().get('user_id'))
    if not place or not user:
        return abort(404)
    elif not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif 'user_id' not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    elif 'text' not in request.get_json():
        return jsonify({"error": "Missing text"}), 400
    new_review = Review(**request.get_json())
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """
    Updates a Place object
    """
    place = storage.get(Place, place_id)
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
