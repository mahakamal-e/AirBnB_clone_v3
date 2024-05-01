#!/usr/bin/python3
"""
Creates a new view for Review object that handles,
all default RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place_id(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]

    return jsonify(reviews), 200


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review_by_id(review_id):
    """Retrieves a Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a Review object by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")

    users = storage.all(User)
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    if "text" not in data:
        abort(400, "Missing text")

    data["place_id"] = place_id
    review = Review(**data)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a Review object by ID"""
    review_by_id = storage.get(Review, review_id)

    if not review_by_id:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    review_by_id.text = body_request.get('text', review_by_id.text)
    storage.save()

    return jsonify(review_by_id.to_dict()), 200
