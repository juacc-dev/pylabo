import sys
import getopt
from pylabo import data, plot, fit, logging

logger = logging.init("pylabo.args")


def parse() -> list[str]:
    try:
        opts, args = getopt.getopt(sys.argv[1:], "pvRl:dr")

    except getopt.GetoptError as err:
        logger.error(err)
        sys.exit(1)

    logger.info("Parsing CLI options.")

    for opt, arg in opts:
        match opt:
            # Don't show plots
            case "-p":
                plot.opts.show = False

            # Verbose
            case "-v":
                logging.set_level(logging.INFO)

            # Regenerate data from Google Sheets
            case "-R":
                data.opt_regen_sheets = True

            # Log file
            case "-l":
                logging.logfile(arg)

            # Show dataframe
            case "-d":
                data.opt_show_dataframe = True

            # Show results
            case "-r":
                fit._helper.opt_show_result = True

            # Default
            case _:
                logger.error("Invalid argument.")

    return args
