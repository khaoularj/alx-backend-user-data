#!/usr/bin/env python3
"""Write a function called filter_datum
that returns the log message obfuscated"""
import re


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}


def filter_datum(fields, redaction, message, separator):
    """functions that returns the log message obfuscated"""
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


if __name__ == "__main__":
    main()
