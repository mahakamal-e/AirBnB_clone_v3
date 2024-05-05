#!/usr/bin/python3
"""Flask web application"""
from flask import Flask, render_template
import uuid
from models import storage

app = Flask(__name__)


@app.route('/0-hbnb/', strict_slashes=False)
def states():
    """Get all state data"""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    users = storage.all("User")

    return render_template("0-hbnb.html",
                           states=states,
                           amenities=amenities,
                           users=users,
                           cache_id=uuid.uuid4())


@app.teardown_appcontext
def terminate(exc):
    """
    To close SQLAlchemy session
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
