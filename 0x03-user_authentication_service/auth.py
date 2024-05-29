#!/usr/bin/env python3
import bcrypt
from bcrypt import hashpw, gensalt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ method that takes in a password string arguments and returns bytes"""
    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """class that interact with the authentication database"""
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """method that register a new user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
