import pandas as pd


def set_if_none(value, default):
    return default if value is None else value


def insert_empty_xerr(df):
    df.insert(1, "", pd.Series())


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
    x = df[cols[0]]
    xerr = df[cols[1]]

    # Y axes and their uncertainty
    ys = [df[col] for col in cols[2::2]]
    yerrs = [df[col] for col in cols[3::2]]

    return x, xerr, ys, yerrs


# def split_df(
#     df: pd.DataFrame
# ):
#     """Get axes from dataframe assuming a struture with one independent
#     variable X and one dependent variables Y, each with their uncertainty, the
#     csv column names would just be
#     ```csv
#     X,X err,Y_1,Y_1 err
#     ```
#     The column for X err has to be there, but it can be empty."""

#     cols = df.columns  # list with column names

#     # X axis and possibly its uncertainty
#     x = df[cols[0]]
#     xerr = df[cols[1]]

#     # Y axes and their uncertainty
#     y = df[cols[2]]
#     yerr = df[cols[3]]

#     return x, xerr, y, yerr


def unpack_df(
    df: pd.DataFrame
):
    x, xerr, ys, yerrs = split_axes(df)

    y_list = [ys[col] for col in ys.columns]
    yerr_list = [yerrs[col] for col in yerrs.columns]

    return x, xerr, *y_list, *yerr_list
