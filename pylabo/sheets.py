import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from pathlib import Path
import logging
import os
from pylabo.lib.opts import Options
import pylabo.csv

logger = logging.getLogger("pylabo.sheets")

opts = Options()
opts.force_download = False

# By default, the service account file is in ~/.config/gspread/creds.json
opts.sa_file = Path(os.environ.get("XDG_CONFIG_HOME")) / "gspread/creds.json"


def open(sheet_id) -> gspread.Spreadsheet:
    """Open a Google Sheets' spreadsheet for reading and writing.

    `sheet_id` is the ID for the spreadsheet, is can fe found in the URL of
    the document after "https://docs.google.com/spreadsheets/d/".
    """

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = Credentials.from_service_account_file(
        opts.sa_file,
        scopes=scopes)

    try:
        logger.debug(f"Searching sheet with ID '{id}'.")

        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(id)

    except gspread.exceptions.SpreadsheetNotFound:
        logger.error(f"Could not find spreadsheet with ID '{id}'.")

    except gspread.exceptions.NoValidUrlKeyFound:
        logger.error(f"Invalid sheet ID: {id}")

    except gspread.exceptions.APIError:
        logger.error(
            "API error. It might be usage limits: for Sheets API v4, this is \
            300 requests per minute per project, and 60 requests per minute \
            per user."
        )

    return spreadsheet


def read(
    worksheet: gspread.Worksheet,
    cellrange: str = None,
    numeric=True
) -> pd.DataFrame:
    """Convert a worksheet or a range of cells into a Pandas dataframe.
    If `cellrange` is not provided, the entire worksheet is used.

    A worksheet can be obtained from a spreadsheet `sheet` as
    ```py
    worksheet = sheet.worksheet("worksheet name")
    ```
    """

    logger.debug("Reading from worksheet.")

    if cellrange is None:
        logger.debug(
            f"Reading all records from worksheet '{worksheet.title}'.")
        return pd.DataFrame(worksheet.get_all_records())

    data = worksheet.get(cellrange)

    headers = data[0]  # Column names
    values = data[1:]  # Actual data

    # Get a list of dicts { header: values } from the list of lists
    records = gspread.utils.to_records(headers, values)

    df = pd.DataFrame(records)

    # This is needed for sheets that represent discrete functions
    if numeric:
        df = df.dropna().astype(float)

        df.sort_values(
            df.columns[0],
            inplace=True,
        )

    return df


def download(
    filename: str,
    sheet_id: str,
    worksheet: gspread.Worksheet,
    cellrange: str = None,
    numeric=True
) -> None:
    """Download a worksheet or a range of cells, but don't do anything if the
    file already exists."""

    file = Path(filename)

    # If the file does not exist, fetch it from Google Sheets
    if not file.is_file() or opts.force_download:
        sheet = open(sheet_id)
        ws = sheet.worksheet(worksheet)

        df = read(
            ws,
            cellrange,
            numeric=numeric
        )

        df.to_csv(
            file,
            sep=pylabo.csv.opts.separator,
            index=False  # disable extra column
        )
