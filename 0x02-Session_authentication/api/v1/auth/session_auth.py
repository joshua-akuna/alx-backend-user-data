#!/usr/bin/env python3

import uuid
from .auth import Auth


class SessionAuth(Auth):
    user_id_by_session_id = {}

    def create_session(self, user_id: str = "Nine") -> str:
        '''Creates a session id for the user id
        '''
        if user_id is None or not isinstance(user_id, str):
            return None

        uid = uuid.uuid4()
        self.user_id_by_session_id[str(uid)] = user_id
        return str(uid)
