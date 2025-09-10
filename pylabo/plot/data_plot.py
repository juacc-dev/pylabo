import pandas as pd
import matplotlib.pyplot as plt
import logging
from matplotlib.axes import Axes

from pylabo.lib.split_axes import split_axes, split_single
from pylabo.lib.utils import set_if_none
from pylabo.plot.utils import axes_are_bad, axis_is_bad, fmt_choice, axis_setup

logger = logging.getLogger("pylabo.plot")


def data(
    df: pd.DataFrame,
    ax=None,
    label=None,
    fmt=None,
    **kwargs
):
    """Plot data from dataframe representing a function of one variable.
    The following structure is assumed:
     - 1st column is the independent variable,
     - 2nd is the uncertainty in the independent variable,
     - 3rd is the dependent variable,
     - 4nd is the uncertainty in the dependent variable.

    Other columns are ignored. The 2nd column (X error) can be empty, but it
    has to be there. """

    x_axis, x_err, y_axis, y_err = split_single(df)

    fig = None

    # ax may be passed. If not, create a new figure
    if ax is None:
        fig, ax = plt.subplots(
            1,
            1,
        )

        axis_setup(
            ax,
            xlabel=x_axis.name,
            ylabel=y_axis.name
        )

    # If passed, ax shuold have the right dimension
    elif axis_is_bad(ax):
        logger.error("Invalid axes argument.")

        return None, None

    # If no fmt is passed, it may be 'o' or '.' depending on the number of
    # points
    fmt = set_if_none(fmt, fmt_choice(x_axis.size))

    # If there is no uncertainty in X, don't plot it
    x_err = x_err if not x_err.isna().all() else None

    if fmt == '.':
        ax.errorbar(
            x_axis,
            y_axis,
            xerr=x_err,
            yerr=y_err,
            label=label,
            fmt=fmt,
            **kwargs
        )

    else:
        ax.plot(
            x_axis,
            y_axis,
            fmt,
            label=label,
            **kwargs
        )
        ax.fill_between(
            x_axis,
            y_axis - y_err,
            y_axis + y_err,
            alpha=0.5
        )

    return fig, ax


def combined(
    df: pd.DataFrame,
    ax=None,
    fmt=None,
    ylabel=None,
    **kwargs
):
    """Multiple plot data from dataframe, each variable is drawn on top the the
    other.
    The following structure is assumed:
     - 1st column is the independent variable,
     - 2nd is the uncertainty in the independent variable,
     - odd columns following are dependent variables,
     - even columns following are the uncertainty in the previous dependent
       variable.
    The 2nd column (X error) can be empty, but it has to be there."""

    x_axis, x_err, y_axes, y_errs = split_axes(df)

    rows = 1
    cols = 1

    fig = None

    # ax may be passed. If not, create a new figure
    if ax is None:
        fig, ax = plt.subplots(
            rows,
            cols,
            sharex=False
        )

        axis_setup(
            ax,
            xlabel=x_axis.name,
            ylabel=ylabel
        )

    # If passed, ax shuold have the right dimension
    elif axis_is_bad(ax):
        logger.error("Invalid axes argument.")

        return None, None

    # fmt may be 'o' or '.' depending on the number of points
    fmt = set_if_none(fmt, fmt_choice(x_axis.size))

    # If there is no uncertainty in X, don't plot it
    x_err = x_err if not x_err.isna().all() else None

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


def stacked(
    df: pd.DataFrame,
    ax=None,
    fmt=None,
    **kwargs
):
    """Multiple plot data from dataframe, each variable is drawn on a separate
    plot, sharing the X axis.
    The following structure is assumed:
     - 1st column is the independent variable,
     - 2nd is the uncertainty in the independent variable,
     - odd columns following are dependent variables,
     - even columns following are the uncertainty in the previous dependent
       variable.
    The 2nd column (X error) can be empty, but it has to be there."""

    x_axis, x_err, y_axes, y_errs = split_axes(df)

    rows = len(y_axes)
    cols = 1

    fig = None

    # ax may be passed. If not, create a new figure
    if ax is None:
        fig, ax = plt.subplots(
            rows,
            cols,
            sharex=True
        )

    # If passed, ax shuold have the right dimension
    elif axes_are_bad(ax, n=len(y_axes.columns)):
        logger.error("Invalid axes argument")

        return None, None

    # fmt may be 'o' or '.' depending on the number of points
    fmt = set_if_none(fmt, fmt_choice(x_axis.size))

    # If there is no uncertainty in X, don't plot it
    x_err = x_err if not x_err.isna().all() else None

    ax[-1].set_xlabel(x_axis.name)

    for axis, y_axis, y_err in zip(ax, y_axes, y_errs):
        axis.errorbar(
            x_axis,
            df[y_axis],
            xerr=x_err,
            yerr=df[y_err],
            **kwargs
        )

        axis_setup(
            axis,
            ylabel=y_axis
        )

    return fig, ax
