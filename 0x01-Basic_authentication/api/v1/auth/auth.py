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
        """if not path.endswith('/'):
            path += '/'"""
        if path[-1] != '/':
            path += '/'
        for items in excluded_paths:
            if items.endswith('*'):
                if path .startswith(p[:1]):
                    return False
        if path in excluded_paths:
            return FRalse
        return True

    def authorization_header(self, request=None) -> str:
        """public method that return the
        authorization header from the request"""
        if request is None:
            return None
        if not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """public method that returns the current user"""
        return None
