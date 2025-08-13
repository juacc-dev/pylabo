import sys
import getopt
import logging
import pylabo.logs as logs

logger = logging.getLogger("pylabo.args")


def parse() -> list[str]:
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vql:Wr")

    except getopt.GetoptError as err:
        logger.error(err)
        sys.exit(1)

    logger.info("Parsing CLI options.")

    for opt, arg in opts:
        match opt:
            # Don't show plots
            # case "-p":
            #     plot.opts.show = False

            # Verbose
            case "-v":
                logs.opts.level_console = logging.DEBUG

            case "-q":
                logs.opts.level_console = logging.ERROR

            # Log file
            case "-l":
                logs.opts.logfile = arg

            # Regenerate data from Google Sheets
            case "-W":
                import pylabo.acquire.sheets as sheets
                sheets.opts.force_download = True

            # Show results
            case "-r":
                import pylabo.analysis.fit as fit
                fit._helper.opt_show_result = True

            # Default
            case _:
                logger.error("Invalid argument.")

    return args
