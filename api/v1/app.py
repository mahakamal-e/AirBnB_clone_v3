#!/usr/bin/python3
""" This app.py file sets up a Flask application
"""
from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def terminate(exc):
    """ Method used to close AQLAlchemy session"""
    storage.close()


@app.errorhandler(404)
def error_not_found(error):
    """handle not found """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    """ main function """
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
