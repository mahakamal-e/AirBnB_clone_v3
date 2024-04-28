#!/usr/bin/python3
""" Place route that handles all default RESTFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_city_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places), 200


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """ Retrieves a Place object by id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Deletes a Place object by id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """ Creates a new Place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    place_data = request.get_json()
    if place_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if not place_data.get('user_id'):
        return jsonify({"error": "Missing user_id"}), 400
    if not place_data.get('name'):
        return jsonify({"error": "Missing name"}), 400

    user = storage.get(User, place_data['user_id'])
    if user is None:
        abort(404)

    place_data['city_id'] = city_id
    new_place = Place(**place_data)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ Update a Place object by place_id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place_data = request.get_json()
    if place_data is None:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at',
                   'updated_at']
    for key, value in place_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()

    return jsonify(place.to_dict()), 200§i
