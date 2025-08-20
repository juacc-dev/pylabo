import pandas as pd
import matplotlib.pyplot as plt
import logging
from matplotlib.axes import Axes

from pylabo.lib.split_axes import split_axes
from pylabo.plot.utils import fmt_choice, axis_setup
from pylabo.lib.utils import set_if_none

logger = logging.getLogger("pylabo.plot")


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
    fmt = set_if_none(fmt, fmt_choice(x_axis.size))

    ax[-1].set_xlabel(x_axis.name)

    for axis, y_axis, y_err in zip(ax, y_axes, y_errs):
        axis.errorbar(
            x_axis,
            df[y_axis],
            xerr=x_err,
            yerr=df[y_err],
            fmt=fmt,
            **kwargs
        )

        axis_setup(
            axis,
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

    rows = 1
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
    fmt = set_if_none(fmt, fmt_choice(x_axis.size))

    ax.set_xlabel(xlabel=x_axis.name)
    ax.set_ylabel(ylabel=ylabel)

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
