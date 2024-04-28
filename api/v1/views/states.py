#!/usr/bin/python3
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


# Retrieves the list of all State objects
@app_views.route('/states', methods=['GET'])
def get_states():
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])

# Retrieves a State object
@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())

# Deletes a State object
@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({}), 404
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

# Creates a State
@app_views.route('/states', methods=['POST'])
def create_state():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201

# Updates a State object
@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200

