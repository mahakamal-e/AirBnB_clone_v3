#!/usr/bin/python3
"""
Create a new view for Review object that handles,
all default RESTFul API actions.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews), 200


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Retrieves a Review object by ID"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object by ID"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates a new Review"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data.keys():
        return jsonify({"error": "Missing user_id"}), 400
    if 'text' not in data:
        return jsonify({"error": "Missing text"}), 400

    users = storage.all(User)
    user_id = users.get('User.' + data['user_id'])
    if user_id is None:
        abort(404)

    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a Review object by ID"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    list_attributes = ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']
    for key, value in data.items():
        if key not in list_attributes:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200

