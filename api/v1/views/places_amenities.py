#!/usr/bin/python3
"""
Creates a new view for the link between Place objects,
and Amenity objects that handles all default RESTFul API actions.
"""
from flask import abort, jsonify, request
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    """ list all Amenity object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify([amenity.to_dict() for amenity in place.amenities])
