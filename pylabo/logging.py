# Help from
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output

import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

log_level = logging.WARNING

class PylaboFormatter(logging.Formatter):
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
        logging.DEBUG:    bold + green + "[Debug]" + format,
        logging.INFO:     bold + cyan + "[Info]" + format,
        logging.WARNING:  bold + magenta + "[Warning]" + format,
        logging.ERROR:    bold + red + "[Error]" + format,
        logging.CRITICAL: bold + bright_red + "[CRITICAL]" + format,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)

        return formatter.format(record)

def init(name):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(PylaboFormatter())

    logger.addHandler(ch)

    return logger


def set_level(level):
    logging.basicConfig(level=level)

def logfile():
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
