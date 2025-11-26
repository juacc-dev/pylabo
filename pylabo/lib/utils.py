import pandas as pd
import logging

logger = logging.getLogger("pylabo.lib.utils")


def set_if_none(value, default):
    return default if value is None else value


def insert_empty_xerr(df):
    df.insert(1, "", pd.Series())


def interpret_df(
    df: pd.DataFrame,
    shape: tuple = (1, None)  # (independent vars, dependent vars)
):
    """Get axes from dataframe assuming a struture with N independent variables
    X_i and M dependent variables Y_j, each with their uncertainty, the csv
    column names would be
    ```csv
    X_1,X_1 err, ... ,X_N, X_N err, Y_1,Y_1 err, ... ,Y_M,Y_M err
    ```
    By default, assume 1 independent variable and the rest dependent."""

    cols = df.columns  # list with column names

    N = shape[0]
    M = shape[1]

    if N is None and M is None:
        logger.error(f"Invalid shape: {shape}")
        raise Exception

    if N is None:
        N = len(cols) - M

    if M is None:
        M = len(cols) - N

    if N + M > len(cols):
        logger.error(f"Invalid shape: {shape}")
        raise Exception

    # X axes and its uncertainty
    x = [df[col] for col in cols[0:2 * N:2]]
    xerr = [df[col] for col in cols[1:2 * N:2]]

    # Y axes and their uncertainty
    y = [df[col] for col in cols[2 * N:2 * (N + M):2]]
    yerr = [df[col] for col in cols[2 * N + 1:2 * (N + M):2]]

    return x, xerr, y, yerr


def unpack_df(
    df: pd.DataFrame
):
    cols = df.columns  # list with column names

    data = (df[col] for col in cols)

    return data
