import matplotlib.pyplot as plt
import pandas as pd
import logging


logger = logging.getLogger("pylabo.plot")


def split_axes(
    df: pd.DataFrame,
    no_xerr=False
):
    """Get axes from dataframe assuming a struture with an independent variable
    X and n dependent variables Y_i, all together with their uncertainty, the
    csv column names would be
    ```csv
    X,X err,Y_1,Y_1 err,Y_2,Y_2 err,...
    ```
    X error may not be there, this is indicatad by the `no_xerr` flag."""

    cols = df.columns  # list with column names

    # X axis and possibly its uncertainty
    x_axis = df[cols[0]]
    x_err = df[cols[1]] if not no_xerr else None

    nx = 1 if x_err is None else 2  # where dependent variables start

    # Y axes and their uncertainty
    y_axes = df[cols[nx::2]]
    y_errs = df[cols[nx+1::2]]

    return x_axis, x_err, y_axes, y_errs
