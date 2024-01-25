#!/usr/bin/env python3
"""
This module contains end-to-end integration tests.
"""
import requests


BASE_URL = 'http://localhost:5000'
ENDPOINTS = {
    "register": "/users",
    "login": "/sessions",
    "profile": "/profile",
    "logout": "/sessions",
    "reset_password": "/reset_password"
}
TEST_USER = {
    "email": "guillaume@holberton.io",
    "password": "b4l0u",
    "new_password": "t4rt1fl3tt3"
}


def make_request(method, endpoint, data=None, cookies=None):
    """
    Makes a request to the specified endpoint with the given data and cookies.

    Args:
        method (str): The HTTP method to use for the request.
        endpoint (str): The endpoint to make the request to.
        data (dict, optional): The data to send with the request.
        cookies (dict, optional): The cookies to send with the request.

    Returns:
        Response: The server's response to the request.
    """
    url = f"{BASE_URL}{ENDPOINTS[endpoint]}"
    return requests.request(method, url, data=data, cookies=cookies)


def register_user(email, password):
    """
    Tests user registration.

    Args:
        email (str): The email of the user to register.
        password (str): The password of the user to register.
    """
    response = make_request(
        "POST",
        "register",
        {
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email, password):
    """
    Tests logging in with a wrong password.

    Args:
        email (str): The email of the user to log in.
        password (str): The wrong password to use for logging in.
    """
    response = make_request(
        "POST",
        "login",
        {
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 401


def log_in(email, password):
    """
    Tests successful logging in.

    Args:
        email (str): The email of the user to log in.
        password (str): The password of the user to log in.

    Returns:
        str: The session ID received from the server.
    """
    response = make_request(
        "POST",
        "login",
        {
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}

    return response.cookies.get("session_id")


def profile_unlogged():
    """
    Tests making a profile request without being logged in.
    """
    response = make_request("GET", "profile", cookies={"session_id": ""})

    assert response.status_code == 403


def profile_logged(session_id):
    """
    Tests making a profile request while being logged in.

    Args:
        session_id (str): The session ID of the logged in user.
    """
    response = make_request(
        "GET",
        "profile",
        cookies={"session_id": session_id}
    )

    assert response.status_code == 200
    assert response.json() == {"email": TEST_USER["email"]}


def log_out(session_id):
    """
    Tests logging out.

    Args:
        session_id (str): The session ID of the user to log out.
    """
    response = make_request(
        "DELETE",
        "logout",
        cookies={"session_id": session_id}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email):
    """
    Tests generating a password reset token.

    Args:
        email (str): The email of the user to generate a password
        reset token for.

    Returns:
        str: The password reset token received from the server.
    """
    response = make_request("POST", "reset_password", {"email": email})

    assert response.status_code == 200

    reset_token = response.json().get("reset_token")

    assert response.json() == {"email": email, "reset_token": reset_token}

    return reset_token


def update_password(email, reset_token, new_password):
    """
    Tests updating a user's password.

    Args:
        email (str): The email of the user to update the password for.
        reset_token (str): The password reset token to use for updating
        the password.
        new_password (str): The new password to set for the user.
    """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = make_request("PUT", "reset_password", data)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(TEST_USER["email"], TEST_USER["password"])
    log_in_wrong_password(TEST_USER["email"], TEST_USER["new_password"])
    profile_unlogged()
    session_id = log_in(TEST_USER["email"], TEST_USER["password"])
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(TEST_USER["email"])
    update_password(TEST_USER["email"], reset_token, TEST_USER["new_password"])
    log_in(TEST_USER["email"], TEST_USER["new_password"])
