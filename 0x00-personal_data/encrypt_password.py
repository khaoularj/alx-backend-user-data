#!/usr/bin/env python3
"""bcrypt hash password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """function that returns a salted,
    hashed password, which is a byte string"""
    personal_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return personal_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """function that checks if it is a hashed pwd"""
    hashed_pwd = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    return hashed_pwd
