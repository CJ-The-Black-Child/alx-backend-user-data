#!/usr/bin/env python3
"""
Auth module for the API
"""
from flask import request
from typing import List, TypeVar


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

        if path in excluded_paths:
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
