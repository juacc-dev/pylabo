import logging


class ConsoleFormatter(logging.Formatter):
    esc = "\x1b["

    reset = esc + "0m"
    bold = esc + "1m"
    red = esc + "31m"
    green = esc + "32m"
    # yellow  = esc + "33m"
    # blue    = esc + "34m"
    magenta = esc + "35m"
    cyan = esc + "36m"
    white = esc + "37m"

    bright_red = esc + "91m"

    format_string = f"{reset} :: {white}(%(name)s){reset} %(message)s"

    FORMATS = {
        logging.DEBUG:    bold + green + "[Debug]" + format_string,
        logging.INFO:     bold + cyan + "[Info]" + format_string,
        logging.WARNING:  bold + magenta + "[Warning]" + format_string,
        logging.ERROR:    bold + red + "[Error]" + format_string,
        logging.CRITICAL: bold + bright_red + "[CRITICAL]" + format_string,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.format_string)
        formatter = logging.Formatter(log_fmt)

        return formatter.format(record)


class FileFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d) :: %(message)s"

        formatter = logging.Formatter(log_fmt)

        return formatter.format(record)
