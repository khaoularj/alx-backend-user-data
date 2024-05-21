#!/usr/bin/env python3
"""class BasicAuth"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar, List


class BasicAuth(Auth):
    """class BasicAuth that inherits from Auth"""
    def extract_base64_authorization_header(
                self,
                authorization_header: str
                ) -> str:
        """method that extracts the base64"""
        if (authorization_header is None or
                not isinstance(authorization_header, str)):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
                self,
                base64_authorization_header: str
                ) -> str:
        """method that decode the base64"""
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
                self,
                decoded_base64_authorization_header: str
                ) -> (str, str):
        """method that extract  user credentials"""
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str)):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, pwd = decoded_base64_authorization_header.split(':', 1)
        return email, pwd

    def user_object_from_credentials(
                self,
                user_email: str,
                user_pwd: str
                ) -> TypeVar('User'):
        """method that returns the User
        instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({"email": user_email})
        if not users:
            return None
        for user in users:
            if not user.is_valid_password(user_pwd):
                return None
        return user
