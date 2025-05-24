# Help from
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output

import logging
from ._formatter import ConsoleFormatter, FileFormatter

logger = logging.getLogger("pylabo.logs")

opts = {
    "console_level": logging.INFO,
    "file_level": logging.DEBUG,
    "logfile": None,
}

def init():
    handlers = []

    console_handler = logging.StreamHandler()

    console_handler.setLevel = opts["console_level"]
    console_handler.setFormatter(ConsoleFormatter())

    handlers.append(console_handler)

    if opts["logfile"] is not None:
        file_handler = logging.FileHandler(opts["logfile"])

        file_handler.setLevel(opts["file_level"])
        file_handler.setFormatter(FileFormatter())

        handlers.append(file_handler)

    logging.basicConfig(handlers=handlers)
