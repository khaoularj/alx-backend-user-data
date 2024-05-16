#!/usr/bin/env python3
"""Write a function called filter_datum
that returns the log message obfuscated"""
import re
import logging
import os
import csv
from typing import List
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initialize the formatter with the fields to redact"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the log record with redacted PII data"""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """functions that returns the log message obfuscated"""
    pattern = r"({})=[^{}]*".format(
        "|".join(map(re.escape, fields)),
        re.escape(separator))
    return re.sub(
        pattern,
        lambda match: "{}={}".format(match.group(1), redaction),
        message)


def get_logger() -> logging.Logger:
    """ return a logger with a RedactingFormatter """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connect to MySQL database """
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
    )


def main():
    """ the main function to fetch data"""
    db_conn = get_db()
    cursor = db_conn.cursor()

    query = (
        "SELECT CONCAT("
        "'name=', name, ';ssn=', ssn, ';ip=', ip, "
        "';user_agent=', user_agent, ';'"
        ") AS message "
        "FROM users;"
    )
    cursor.execute(query)

    logger = get_logger()

    for row in cursor:
        logger.info(row[0])

    cursor.close()
    db_conn.close()


if __name__ == "__main__":
    main()
