#!/usr/bin/env python3
"""
This module defines the API routes for the authentication service.
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect
app = Flask(__name__)
AUTH = Auth()


@app.routee('/', methods=['GET'])
def hello_world() -> str:
    """
    The base route for the authentication service API.

    Returns:
        str: A welcome message in JSON format.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user() -> str:
    """
    Registers a new user if they do not exist

    Returns:
        str: A message indicating the result of the registration
        in JSON format.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        abort(400)

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({
            "message": "email already registered"
        }), 400
    return jsonify({
        "email": email,
        "message": "user created"
    })


@app.route('/sessions', methods=['POST'])
def log_in() -> str:
    """
    Logs in a user and returns a session ID.

    Returns:
        str: A message indicating the result of the login in JSON format.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password or not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({
        "email": email, "message": "logged in"
    })
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def log_out() -> str:
    """
    Logs out a user and redirects them to the base route

    Returns:
        str: A redirection to the base route.
    """
    session_id = request.cookies.get("session_id")

    if session_id is None or AUTH.get_user_from_session_id(session_id) is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """
    Retrieves the profile of a user.

    Returns:
        str: The user's email in JSON format.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if session_id is None or user is None:
        abort(403)

    return jsonify({
        "email": user.email
    }), 200


@app.route("/reset_password", methods=["POST"])
def reset_password() -> str:
    """
    Generates a reset password token for a user.

    Returns:
    str: A message indicating the result of the operation in JSON format.
    """
    email = request.get_json().get("email")

    if email is None:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({
        "email": email, "reset_token": reset_token
    }), 200


@app.route("/reset_password", methods=["PUT"])
def update_password() -> str:
    """
    Updates a user's password using a reset token.

    Returns:
        str: A message indicating the result of the operation in JSON format.
    """
    data = request.get_json()
    email = data.get("email")
    reset_token = data.get("reset_token")
    new_password = data.get("new_password")

    if not email or not reset_token or not new_password:
        abort(400)

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({
        "email": email,
        "message": "Password updated"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
