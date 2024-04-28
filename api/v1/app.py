#!/usr/bin/python3
""" This app.py file sets up a Flask application
"""
from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

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
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', 5000),
            threaded=True)
