#!/usr/bin/env python3
"""
Defines a hash_password and is_valid functions
"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """
    Returns a hashed password
    Args:
        password: password to be hashed
    Return:
        bytes
    """
    enc_pwd = password.encode()
    hash_pwd = hashpw(enc_pwd, bcrypt.gensalt())
    return hash_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check whether a password is valid
    Args:
        hashed_password (bytes): hashed password
        password (str): password in string
    Return:
        bool
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
