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
    sep=opts.separator,
    **kwargs
) -> pd.DataFrame:
    """Load a csv file. It is just a simple wrapper for Pandas."""

    df: pd.DataFrame

    file = Path(filename)

    logger.debug(f"Reading '{file}'.")

    try:
        df = pd.read_csv(file, sep=sep, **kwargs)

    except FileNotFoundError:
        logger.error(f"The file '{file}' does not exist")

    return df


def save_from_dict(
    data: dict,
    filename: Path | str,
    orient: str = "columns",
    sep=opts.separator,
    **kwargs
) -> None:
    """Simple wrapper to save results stored in a dict."""

    data = [data] if orient == "columns" else data

    # Convert dictionary to dataframe
    df = pd.DataFrame.from_dict(data, orient=orient)

    logger.info(f"Saving results to '{filename}'")

    # Save
    df.to_csv(
        filename,
        index=False if orient == "columns" else True,
        sep=sep,
        **kwargs
    )
