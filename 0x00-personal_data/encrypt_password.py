#!/usr/bin/env python3
"""
A module for encrypting passwords.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using a random salt.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt(password.encode(), salt)
    return hashed
