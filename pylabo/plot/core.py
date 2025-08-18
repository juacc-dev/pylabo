import matplotlib.pyplot as plt
import pandas as pd
import logging
import pylabo.plot.utils as utils
from pylabo.lib.utils import set_if_none

# Types
from matplotlib.axes import Axes

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


def show():
    """A not very useful wrapper."""

    plt.show()
    plt.close()


def stacked(
    df: pd.DataFrame,
    no_xerr=False,
    fig=None,
    ax=None,
    fmt=None,
    **kwargs
):
    """Plot a dataframe assuming the same structure as in split_axes().
    Each dependent variable is on a different plot, sharing X axis."""

    x_axis, x_err, y_axes, y_errs = split_axes(df, no_xerr=no_xerr)

    rows = len(y_axes)
    cols = 1

    # fig and ax may be passed. If not, create them
    if fig is None and ax is None:
        fig, ax = plt.subplots(
            rows,
            cols,
            sharex=True
        )

    # If passed, ax shuold have the right dimension
    elif len(ax) != len(y_axes.columns):
        logger.error(f"Passed axes of incorrect size. Expected {
                     y_axes.ndim}, got {len(ax)}")

        return None, None

    # fmt may be 'o' or '.' depending on the number of points
    fmt = set_if_none(fmt, utils.fmt_choice(x_axis.size))

    ax[0].set_xlabel(x_axis.name)

    for axis, y_axis, y_err in zip(ax, y_axes, y_errs):
        axis.errorbar(
            x_axis,
            df[y_axis],
            xerr=x_err,
            yerr=df[y_err],
            fmt=fmt,
            **kwargs
        )

        axis.set(
            ylabel=y_axis
        )

    return fig, ax


def combined(
    df: pd.DataFrame,
    no_xerr=False,
    fig=None,
    ax=None,
    fmt=None,
    ylabel=None,
    **kwargs
):
    """Plot a dataframe assuming the same structure as in split_axes().
    All dependent variables are on the same plot, sharing X axis."""

    x_axis, x_err, y_axes, y_errs = split_axes(df, no_xerr=no_xerr)

    rows = len(y_axes)
    cols = 1

    # fig and ax may be passed. If not, create them
    if fig is None and ax is None:
        fig, ax = plt.subplots(
            rows,
            cols,
            sharex=False
        )

    # If passed, ax shuold have the right dimension
    elif type(ax) is not Axes:
        logger.error("Invalid axes argument.")

        return None, None

    # fmt may be 'o' or '.' depending on the number of points
    fmt = set_if_none(fmt, utils.fmt_choice(x_axis.size))

    ax.set(
        xlabel=x_axis.name,
        ylabel=ylabel
    )

    for y_axis, y_err in zip(y_axes, y_errs):
        ax.errorbar(
            x_axis,
            df[y_axis],
            xerr=x_err,
            yerr=df[y_err],
            fmt=fmt,
            label=y_axis,
            **kwargs
        )

    return fig, ax
