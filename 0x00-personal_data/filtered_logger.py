#!/usr/bin/env python3

""""The module defines the filtered datum function"""
import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum"""
        msg = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(self.fields, RedactingFormatter.REDACTION,
                                msg, RedactingFormatter.SEPARATOR)
        return redacted


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """The function uses regex to replace occurences of certain
        field values

        Args
            fields: a list of string representing fields to ofuscate
            redaction: represent the string by what the field
                        will be ofuscated
            message: represents the log line to ofuscate
            separator: represents a string which separate all strings
                        in the log line
    """
    for field in fields:
        message = re.sub(field + '=.*?' + separator,
                         field + '=' + redaction + separator, message)
    return message


def get_logger() -> logging.Logger:
    '''returns a logging.Logger object
    '''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    fmt = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(fmt)
    logger.addHandler(handler)

    return logger


def _get_db() -> mysql.connector.connection.MySQLConnection:
    '''Connects to a MySQL server
    '''
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    db_pass = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    db_host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    db_conn = mysql.connector.connect(user=db_user,
                                      password=db_pass,
                                      host=db_host,
                                      database=db_name)

    return db_conn


def get_db() -> mysql.connector.connection.MySQLConnection:
    """connects to the musql database
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(user=user,
                                   password=passwd,
                                   host=host,
                                   database=db_name)
    return conn
