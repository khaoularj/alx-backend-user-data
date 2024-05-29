#!/usr/bin/env python3
import bcrypt
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """ method that takes in a password string arguments and returns bytes"""
    return hashpw(password.encode('utf-8'), gensalt())
