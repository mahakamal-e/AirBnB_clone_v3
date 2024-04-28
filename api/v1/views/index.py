#!/usr/bin/python3
""" This Module contains the route definitions,
for your API endpoints."""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})
