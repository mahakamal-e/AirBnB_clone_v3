#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template
import uuid

app = Flask(__name__)


@app.route('/2-hbnb/', strict_slashes=False)
def hbnb():
    """ HBNB is alive! """
    states = storage.all("State")
    amenities = storage.all("Amenity")
    users = storage.all("User")
    cache_id = (str(uuid.uuid4()))
    return render_template("2-hbnb.html",
                           states=states,
                           amenities=amenities,
                           users=users,
                           cache_id=uuid.uuid4())


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
