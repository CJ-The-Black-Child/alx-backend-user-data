#!/usr/bin/env python3
"""
This module handles user authentication. It provides functionalities such as
user registration, login validation, session management, and password reset.
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union, Optional
from user import User
from uuid import uuid4


def _hash_password(password: str) -> str:
    """
    Hashes the input password with a salt using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a new UUID.

    Returns:
        str: The string representation of the new UUID.
    """
    return str(uuid4())


class Auth:
    """
    This class provides methods to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user in the database.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The newly registered user.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates the user's login credentials.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Optional[str]:
        """
        Creates a new session for the user.

        Args:
            email (str): The user's email.

        Returns:
            Optional[str]: The session ID if the user exists, None otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        Retrieves the user from the session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            Optional[User]: The user if the session ID is valid, None
            otherwise.
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys the user's session.

        Args:
            user_id (int): The user's ID.
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token for the user.

        Args:
            email (str): The user's email.

        Returns:
            str: The reset password token.

        Raises:
            ValueError: If the user does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates the user's password using the reset token.

        Args:
            reset_token (str): The reset password token.
            password (str): The new password.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                user.id,
                hashed_password=hashed_password,
                reset_token=None
            )
        except NoResultFound:
            raise ValueError
