#!/usr/bin/env python3
"""
Filtering logs
"""
import re
from typing import List
import logging



PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Log line filtering
    """
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]*", f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"

    def __init__(self, fields):
        super().__init__(self.FORMAT)
        self.fields = fields
        self.pattern = re.compile(f'({"|".join(fields)})=[^;]*')

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        return self.pattern.sub(r"\1=" + self.REDACTION, message)

def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger

if __name__ == "__main__":
    main()
