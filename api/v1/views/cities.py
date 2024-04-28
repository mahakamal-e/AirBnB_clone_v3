#!/usr/bin/python3
"""
Creates new view for City objects that handles
all default RESTFul API actions.
"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities/', methods=['GET'])
def get_cities_by_state(state_id):
    """
    Retrieves the list of all City objects of a State.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities), 200


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a City object."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    """Method that Creates a City."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city_name = request.get_json()
    if not city:
        return jsonify({"Not a JSON"}), 400
    if not city_name.get('name'):
        return jsonify({"Missing name"}), 400
    city_name['state_id'] = state_id
    new_city = City(**city_name)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a City object.
    with new value
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    req_city = request.get_json()
    if not req_city:
        return jsonify({"Not a JSON"}), 400
    setattr(city, 'name', req_city.get('name'))
    storage.save()
    return jsonify(city.to_dict()), 200
