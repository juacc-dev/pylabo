from pathlib import Path
import pandas as pd
import logging
from pylabo import utils

logger = logging.getLogger(__name__)

DATA_DIR = "data"
RESULTS_DIR = "results"

opt_regen_sheets = False
opt_show_dataframe = False


def generate(
    path: Path | str,
    worksheet: str,
    cellrange: str
) -> pd.DataFrame:
    """
    Generate and save dataframe from Google Sheets
    """

    logger.warning("Fetching Google Sheets.")

    from common import sheets

    ws = sheets.open_sheet(path).worksheet(worksheet)

    logger.info("Creating dataframe.")

    # Need to test ws.get_all_records
    df = sheets.get_dataframe(
        ws,
        cellrange=cellrange
    ).dropna().astype(float)

    df.sort_values(
        df.columns[0],
        inplace=True,
    )

    return df


def load(
    filename: str,          # Local file name
    # wsname: str = None,     # Worksheet name
    # cellrange: str = None,  # e.g. "A2:C41"
    **kwargs
) -> pd.DataFrame:
    """
    Search for a csv file in "path/data/". If it doesn't exist, or "-R" was
    passed to the program, search in Sheets; unless `nosheet` was passed as
    True. `wsname` is the name of the worksheet: if not specified, look for a
    worksheet named the same as `module`.
    """

    # Path and filename of the calling script
    # path, name = utils.get_caller_name()

    df: pd.DataFrame

    # If searching for a local file
    # if filename is not None:
        # csv_file = path / DATA_DIR / file

    file = Path(filename)

    # If there is no existing dataframe (or chose to regenerate), create it
    if not file.is_file():
        # stem = name + ".csv"

        # Where the dataframe should be stored
        # csv_file = path / DATA_DIR / stem

        logger.error(f"Could not find '{file}'.")

        # else:
        #     logger.info(
        #         f"Found file for '{
        #             stem}'. Using gspread anyways since '-R' was passed."
        #     )

        # Create dataframe
        # df = generate(
        #     path,
        #     name if not wsname else wsname,
        #     cellrange
        # )

        # Save file. `index=False` to disable extra column.
        # df.to_csv(
        #     csv_file,
        #     index=False
        # )

    # This can't be removed when generating the dataframe,
    # it does not work for some reason.
    logger.info(f"Reading '{file}'.")
    df = pd.read_csv(file, **kwargs)

    if opt_show_dataframe:
        print(f"Showing dataframe for file '{file}':")
        print(df.to_string())

    return df


def save(
    data: dict,
    filename: Path | str = None,
    append: str = None
    # sheet: str = None
) -> None:
    """
    Simple wrapper to save results.
    """

    # Convert dictionary to dataframe
    df = pd.DataFrame(data)

    if filename is None:
        path, name = utils.get_caller_name()

        filename = path / f"{RESULTS_DIR}/{name}.csv"

    # if append is not None:
    #     new_name = f"{filename.stem}-{append}"
    #     filename = filename.parent / f"{new_name}.csv"

    logger.info(f"Saving results to '{filename}'")

    if opt_show_dataframe:
        print(f"'{filename}' results dataframe:")
        print(df)

    # Save
    df.to_csv(
        filename,
        index=False
    )

    # Upload to Google Sheets
    # if sheet is not None:
    #     logger.warning("Uploading to Google Sheets.")
