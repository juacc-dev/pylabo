from lib import arguments
import logging
import sys

logger = logging.getLogger(__name__)


def main() -> None:
    args = arguments.parse(sys.argv[1:])

    match args[0]:
        case "sub":
            from src import 


if __name__ == "__main__":
    main()
