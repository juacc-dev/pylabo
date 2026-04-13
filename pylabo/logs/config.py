import logging
from pylabo.lib.opts import Options
from pylabo.logs.formatter import ConsoleFormatter, FileFormatter

# Default options
opts = Options()
opts.level_console = logging.WARNING
opts.level_file = logging.DEBUG
opts.logfile = None

handlers = []

def setup():
    # Define handlers. By default, only log to the console.
    console_handler = logging.StreamHandler()

    console_handler.setLevel(opts.level_console)
    console_handler.setFormatter(ConsoleFormatter())

    handlers.append(console_handler)

    if opts.logfile is not None:
        file_handler = logging.FileHandler(opts.logfile)

        file_handler.setLevel(opts.level_file)
        file_handler.setFormatter(FileFormatter())

        handlers.append(file_handler)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    for handler in handlers:
        root_logger.addHandler(handler)
