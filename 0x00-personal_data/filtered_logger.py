#!/usr/bin/env python3

""""The module defines the filtered datum function"""
import re
from typing import List
import logging


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
