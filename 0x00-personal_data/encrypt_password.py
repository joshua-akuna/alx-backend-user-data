#!/usr/bin/env python3
"""The module defines the hash_password and is_valid functions"""

import bcrypt


def hash_password(passwd: str) -> bytes:
    """ takes a password string and returns the hashed password
        in bytes
    """
    pwd = passwd.encode()
    pwd_hash = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return pwd_hash


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks if password is valid"""
    return bcrypt.checkpw(password.encode(), hashed_password)
