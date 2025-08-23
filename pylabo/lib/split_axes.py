import pandas as pd


def split_axes(
    df: pd.DataFrame
):
    """Get axes from dataframe assuming a struture with an independent variable
    X and n dependent variables Y_i, all together with their uncertainty, the
    csv column names would be
    ```csv
    X,X err,Y_1,Y_1 err,Y_2,Y_2 err,...
    ```
    The column for X err has to be there, but it can be empty."""

    cols = df.columns  # list with column names

    # X axis and possibly its uncertainty
    x_axis = df[cols[0]]
    x_err = df[cols[1]]

    # Y axes and their uncertainty
    y_axes = df[cols[2::2]]
    y_errs = df[cols[3::2]]

    return x_axis, x_err, y_axes, y_errs


def split_single(
    df: pd.DataFrame
):
    """Get axes from dataframe assuming a struture with one independent
    variable X and one dependent variables Y, each with their uncertainty, the
    csv column names would just be
    ```csv
    X,X err,Y_1,Y_1 err
    ```
    The column for X err has to be there, but it can be empty."""

    cols = df.columns  # list with column names

    # X axis and possibly its uncertainty
    x_axis = df[cols[0]]
    x_err = df[cols[1]]

    # Y axes and their uncertainty
    y_axis = df[cols[2]]
    y_err = df[cols[3]]

    return x_axis, x_err, y_axis, y_err
