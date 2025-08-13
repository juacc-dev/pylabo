# Help from:
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output

import logging
from lib.opts import Options
from pylabo.logs.formatter import ConsoleFormatter, FileFormatter

logger = logging.getLogger("pylabo.logs")

opts = Options()
opts.level_console = logging.INFO,
opts.level_file = logging.DEBUG,
opts.logfile = None,

handlers = []

console_handler = logging.StreamHandler()

console_handler.setLevel = opts.level_console
console_handler.setFormatter(ConsoleFormatter())

handlers.append(console_handler)

if opts.logfile is not None:
    file_handler = logging.FileHandler(opts.logfile)

    file_handler.setLevel(opts.level_file)
    file_handler.setFormatter(FileFormatter())

    handlers.append(file_handler)

    logging.basicConfig(handlers=handlers)
