#!/usr/bin/python3
""" This Module contains the route definitions,
for your API endpoints."""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """ returns status of program """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_objects_counts():
    """Retrieves the number of each objects by type."""
    object_types = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }

    counts = {
        object_type: storage.count(cls)
        for object_type, cls in object_types.items()
    }

    return jsonify(counts)
