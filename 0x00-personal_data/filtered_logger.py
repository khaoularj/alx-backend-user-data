#!/usr/bin/env python3
"""Write a function called filter_datum
that returns the log message obfuscated"""
import re


def filter_datum(fields, redaction, message, separator):
    """functions that returns the log message obfuscated"""
    pattern = r'({}|^)({}=[^{}]+{})'.format(
        re.escape(separator), '|'.join(fields), separator, separator
    )

    return re.sub(
        pattern,
        lambda match: '{}{}'.format(
            match.group(1),
            '{}={}'.format(match.group(2).split(separator)[0], redaction)
        ),
        message
    )
