#!/usr/bin/env python3
"""
Session Auth view
"""
from flask import Flask, request, jsonify, abort
from api.v1.app import auth
from models.user import User

app = Flask(__name__)


@app.route("/api/v1/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Logout by deleting the Session ID contains in the request as cookie 
    """
    success = auth.destroy_session(request)
    if not success:
        abort(404)

    return jsonify({}), 200