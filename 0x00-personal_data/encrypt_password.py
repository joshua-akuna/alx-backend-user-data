#!/usr/bin/env python3
"""The module defines the hash_password and is_valid functions"""

import bcrypt
from bcrypt import hashpw


def hash_password(passwd: str) -> bytes:
    """ takes a password string and returns the hashed password
        in bytes
    """
    enc_pwd = password.encode()
    hashed = hashpw(enc_pwd, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks if password is valid"""
    return bcrypt.checkpw(password.encode(), hashed_password)
