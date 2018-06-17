from termcolor import colored
from lib.helper import current_time
# from src import SENTRY_CLIENT
# from date_is_very_complicated import current_time


def logger(message, level=None, color=None):
    """
    Wrapping and formatting print out and/or sending error to Sentry.
    :param message: <string> log message.
    :param level: <string> set 'Error' for capture to Sentry. Default 'Message'.
    :param color: ANSII Color formatting for output in terminal.
    :return: None
    """
    if level and level.lower() == 'error':
        # SENTRY_CLIENT.captureException()
        # color = 'red'
        pass
    if color:
        print colored('[{date}] -- {message}'.format(date=current_time(), message=message), color)
    else:
        print '[{date}] -- {message}'.format(date=current_time(), message=message)
