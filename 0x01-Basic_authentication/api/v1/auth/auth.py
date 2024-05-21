#!/usr/bin/env python3
"""creating the class Auth to manage the API authentication"""
from flask import request
from typing import List, TypeVar


class Auth():
    """class that manage the API authenticatio"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method that check if authentication is required"""
        if path is None or not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        for items in excluded_paths:
            if items.endswith('/'):
                if path == items:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """public method that return the
        authorization header from the request"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """public method that returns the current user"""
        return None
