#!/usr/bin/python3
""" States route that handles all default RESTFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """ list all states """
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]

    return jsonify(states_list), 200


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a state by id """
    state = storage.get(State, state_id)
    if state is None:
        response = jsonify({"error": "Not found"})
        response.status_code = 404
        return response
    return jsonify(state.to_dict()), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """ creates new state """
    state = request.get_json()

    if state is None:
        return jsonify({"error": "Not a JSON"}), 400
    if not state.get('name'):
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**state)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes state by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update a state by state_id."""
    current_state = storage.get(State, state_id)
    if current_state is None:
        return jsonify({"error": "Not found"}), 404
    new_state = request.get_json()

    if not new_state:
        return jsonify({"error": "Not a JSON"}), 400
    setattr(current_state, 'name', new_state.get('name'))
    storage.save()
    return jsonify(current_state.to_dict()), 200
