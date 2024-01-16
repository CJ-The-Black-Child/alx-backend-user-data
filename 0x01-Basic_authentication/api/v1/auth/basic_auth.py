#!/usr/bin/env python3
"""
BasicAuth module for the API
"""
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        Method to extract the Base64 Authorization
        """
        if authorization_header is None or type(
            authorization_header
        ) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Method to decode the Base64 Authorization
        """
        if (
            base64_authorization_header is None or type(
                base64_authorization_header
            ) is not str
        ):
            return None
        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            message_bytes = base64.b64decode(base64_bytes)
            return message_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Method to extract the user credentials
        """
        if (
            decoded_base64_authorization_header is None or type(
                decoded_base64_authorization_header
            ) is not str
        ):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        separator = decoded_base64_authorization_header.find(":")
        user_email = decoded_base64_authorization_header[:separator]
        user_pwd = decoded_base64_authorization_header[separator + 1:]
        return user_email, user_pwd

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """
        Method to get the User instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            users = User.search({
                "email": user_email
            })
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to retrieve the User instance for a request
        """
        header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        user_credentials = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(
            user_credentials[0], user_credentials[1]
        )
