from common import cli_args
import logging
import sys

logger = logging.getLogger(__name__)


def main() -> None:
    args = cli_args.parse(sys.argv[1:])

    # What to do
    match args[0]:
        case "show":
            from src import show
            show.main(args)

        case "abs":
            from src import absorb
            absorb.main(args)

        case "comp":
            from src import comp
            comp.main(args)

        case _:
            logger.error("Invalid argument")


if __name__ == "__main__":
    main()
