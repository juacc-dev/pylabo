import pandas as pd
import logging

logger = logging.getLogger("pylabo.proc.dataframe")


def strip_channel(
    df: pd.DataFrame,
    channel: int,
):
    """
    Return a dataframe with only 4 columns corresponding to:
      1. X axis,
      2. X error,
      3. Y axis,
      4. Y error.
    """

    # 'Y error' is assumed to be next to 'Y'.
    df_stripped = df[[0, 1, channel, channel + 1]]

    return df_stripped


def unpack_df(
    df: pd.DataFrame
):
    """
    Split a dataframe into its columns. This function returns a tuple of numpy
    arrays, each array being a column.
    """
    cols = df.columns  # A list with all the column names

    data = (df[col].to_numpy() for col in cols)

    return data


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


def df_to_pair(df: pd.DataFrame):
    """
    Assume 1 independent variable and 1 dependent variable.
    Return those two variables, without their error
    """
    xs, _, ys, _ = interpret_df(df, shape=(1, 1))

    x = xs[0]
    y = ys[0]

    return x, y


def pair_or_df(
    x_or_df,
    y
):
    if y is None:
        df = x_or_df
        x, y = df_to_pair(df)

    else:
        x = x_or_df

    return x, y
