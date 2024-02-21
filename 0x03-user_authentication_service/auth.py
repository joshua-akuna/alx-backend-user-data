#!/usr/bin/env python3
"""auth.py
"""

import bcrypt
from db import DB
from user import User
from uuid import uuid4

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


def _generate_uuid() -> str:
    """returns the string representation of a new uuid

        Returns: a new uuid
    """
    return str(uuid4())


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

    def create_session(self, email: str) -> str:
        """finds the user corresponding to the email, generate a new
            UUID and store it in the database as the user's session_id


            Arg:
                email (str): email of the user

            returns:
                generated UUID for the user session
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            user.session_id = _generate_uuid()
            return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """returns the corresponding user with session_id or None

            Args:
                session_id (str): session_id of User to return

            returns: User instance with session_id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id: str) -> None:
        """The method updates the corresponding user
            session_id to None

        Args:
            user_id (str): user id to whose session to update

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        else:
            user.session_id = None
            return None
