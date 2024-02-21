#!/usr/bin/env python3
"""auth.py
"""

import bcrypt
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash the input password using bcrypt with a salt

    Args:
        password (str): The input password string

    Returns:
        bytes: Salted hash of the input password
    """
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd


class Auth():
    """Auth class to interact with authentication database
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register new user with email and password

        Args:
            email (str): User's email
            password (str): User's password

        Returns:
            User object representing the new User

        Raises:
            ValueError: If a user with the same email already exists
        """
        try:
            # find user by email
            self._db.find_user_by(email=email)
        except NoResultFound:
            # adds user to db if no result is found
            return self._db.add_user(email, _hash_password(password))
        else:
            # raise error if user already exists
            raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """validates a user login credentials

            Args:
                email (str): the email of the user
                password (str): the password of the user

            Returns:
                Boolean: True if credential is valid else False
        """
        try:
            # find the user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        # validate user password
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
