#!/usr/bin/env python3

"""
Main file
"""
from auth import Auth

auth = Auth()
email = 'bob@bob.com'
password = 'MyPowOfBob'

auth.register_user(email, password)

print(auth.create_session(email))
print(auth.create_session('unknown@email.com'))
