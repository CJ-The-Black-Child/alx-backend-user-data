#!/usr/bin/env python3
"""
Filtering logs
"""
import re
from typing import List

def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Log line filtering
    """
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]*", f"{field}={redaction}", message)
    return message