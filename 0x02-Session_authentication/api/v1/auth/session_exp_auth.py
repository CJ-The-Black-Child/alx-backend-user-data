#!/usr/bin/env python3
"""
SessionExpAuth module
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class that inherits from SessionAuth
    """

    def __init__(self):
        """
        Initialize a SessionExpAuth instance
        """
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """
        Create a Session ID and its expiration date
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return a User ID based on a Session ID
        """
        if session_id is None:
            return None

        user_id = session_dictionary.get("user_id")
        if user_id is None:
            return None

        if self.session_duration <= 0:
            return user_id

        created_at = session_dictionary.get("created_at")
        if created_at is None:
            return None

        session_duration = timedelta(seconds=self.session_duration)
        expiration_date = created_at + session_duration

        if datetime.now() >= expiration_date:
            return None

        return user_id