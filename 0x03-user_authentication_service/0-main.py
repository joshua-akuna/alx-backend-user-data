#!/usr/bin/env python3
"""
Main File
"""
from user import User

print(User.__tablename__)

for col in User.__table__.columns:
    print("{}: {}".format(col, col.type))
