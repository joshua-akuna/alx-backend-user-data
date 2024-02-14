#!/usr/bin/env python3
"""Defines the SessionAuth class
"""

import uuid
from .auth import Auth


class SessionAuth(Auth):
    """Authenticates users by session
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = "Nine") -> str:
        '''Creates a session id for the user id
        '''
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        uid = uuid.uuid4()
        self.user_id_by_session_id[str(uid)] = user_id
        return str(uid)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user by its session id
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)
