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


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """retrieves count of each objects 
    """
    objects = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
        }

    count_objects = {
      key: storage.count(value) for key, value in objs.items()
    }

    return jsonify(count_objects)
