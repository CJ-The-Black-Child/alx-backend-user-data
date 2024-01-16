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
        return False


    def authorization_header(self, request=None) -> str:
        """
        Method to handle authorization header
        """
        None


    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to handle current user
        """
        return None