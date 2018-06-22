# -*- coding: utf-8 -*-
from datetime import datetime


def is_numeric(value):
    try:
        return isinstance(long(value), long)
    except ValueError:
        return False


def is_string(value):
    try:
        return isinstance(str(value), long)
    except ValueError:
        return False


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    pass
