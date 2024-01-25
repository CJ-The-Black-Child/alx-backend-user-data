#!/usr/bin/env python3
"""
This module defines the User model for the database.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    """
    Represents a record from the users table.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self) -> str:
        """
        Returns a string representation of the User instance.

        Returns:
            str: A string representation of the User instance.
        """
        return (
            f"< User("
            f"email='{self.email}',"
            f"hashed_password='{self.hashed_password}',"
            f"session_id='{self.session_id}',"
            f"reset_token='{self.reset_token}'"
            f") >"
        )
