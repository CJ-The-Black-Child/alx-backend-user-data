#!/usr/bin/env python3
"""
Auth module for the API
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    This class does manage the API Auth
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to require auth
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        if path[-1] != "/":
            path += "/"

        for exc in excluded_paths:
            if exc[-1] == "*":
                if path.startswith(exc[:-1]):
                    return False
            elif path == exc:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to handle authorization header
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to handle current user
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Returns the value of the cookie named _my_session_id from the request
        """
        if request is None:
            return None

        session_name = os.environ.get("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
