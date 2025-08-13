from pathlib import Path
import pandas as pd
import logging
from lib.opts import Options

logger = logging.getLogger("pylabo.csv")

DATA_DIR = "data"
RESULTS_DIR = "results"

opts = Options()
opts.separator = ','


def load(
    filename: str,
    **kwargs
) -> pd.DataFrame:
    """Load a csv file. It is just a simple wrapper for Pandas."""

    # df: pd.DataFrame

    file = Path(filename)

    # This can't be removed when generating the dataframe,
    # it does not work for some reason.
    logger.debug(f"Reading '{file}'.")

    try:
        df = pd.read_csv(file, **kwargs)

    except FileNotFoundError:
        logger.error(f"The file '{file}' does not exist")

    # print(f"Showing dataframe for file '{file}':")
    # print(df.to_string())

    return df


def save_from_dict(
    data: dict,
    filename: Path | str
) -> None:
    """Simple wrapper to save results stored in a dict."""

    # Convert dictionary to dataframe
    df = pd.DataFrame(data)

    logger.info(f"Saving results to '{filename}'")

    # Save
    df.to_csv(
        filename,
        index=False
    )
