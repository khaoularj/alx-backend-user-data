#!/usr/bin/env python3
"""Module for user authentication"""
import bcrypt
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """ method that takes in a password string arguments and returns bytes"""
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """method that generates a new UUID and returns it as a string"""
    return str(uuid.uuid4())


class Auth:
    """the class Auth that interact with the authentication database"""
    def __init__(self):
        """init method"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """method that register a new user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """method that check if the login credentials"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """method that create a session for a user"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """method that get a user from the session ID"""
        if session_id is None or session_id == '':
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """method that destroy a user's session"""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """method to reset password token for the user"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """method that update the password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
