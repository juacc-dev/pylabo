# Help from
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output

import logging as python_logging

DEBUG = python_logging.DEBUG
INFO = python_logging.INFO
WARNING = python_logging.WARNING
ERROR = python_logging.ERROR
CRITICAL = python_logging.CRITICAL

def log_level(level=None):
    if "level" not in log_level.__dict__:
        log_level.__dict__["level"] = INFO

    if level is not None:
        log_level.level = level

    return log_level.level


class PylaboFormatter(python_logging.Formatter):
    esc = "\x1b["

    reset   = esc + "0m"
    bold    = esc + "1m"
    red     = esc + "31m"
    green   = esc + "32m"
    # yellow  = esc + "33m"
    # blue    = esc + "34m"
    magenta = esc + "35m"
    cyan    = esc + "36m"
    white   = esc + "37m"

    bright_red = esc + "91m"

    format = f"{reset} :: {white}(%(name)s) {reset} %(message)s"

    FORMATS = {
        DEBUG:    bold + green + "[Debug]" + format,
        INFO:     bold + cyan + "[Info]" + format,
        WARNING:  bold + magenta + "[Warning]" + format,
        ERROR:    bold + red + "[Error]" + format,
        CRITICAL: bold + bright_red + "[CRITICAL]" + format,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = python_logging.Formatter(log_fmt)

        return formatter.format(record)

def init(name):
    logger = python_logging.getLogger(name)
    logger.setLevel(log_level())

    ch = python_logging.StreamHandler()
    ch.setLevel(python_logging.DEBUG)

    ch.setFormatter(PylaboFormatter())

    logger.addHandler(ch)

    return logger


def set_level(level):
    python_logging.basicConfig(level=level)
    log_level(level)

def logfile():
    python_logging.basicConfig(
        filename='example.log',
        encoding='utf-8',
        level=DEBUG
    )
