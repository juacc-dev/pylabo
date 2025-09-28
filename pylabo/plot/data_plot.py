import pandas as pd
import matplotlib.pyplot as plt
import logging

from pylabo.lib.utils import split_axes, set_if_none
from pylabo.plot.utils import axes_bad_type, axis_bad_type, fmt_choice

logger = logging.getLogger("pylabo.plot")


def _plot(
    ax,
    x_axis,
    y_axis,
    xerr,
    yerr,
    fmt,
    label=None,
    **kwargs
):
    if fmt == '.':
        ax.errorbar(
            x_axis,
            y_axis,
            xerr=xerr,
            yerr=yerr,
            label=label,
            fmt=fmt,
            **kwargs
        )

    else:
        ax.errorbar(
            x_axis,
            y_axis,
            xerr=xerr,
            yerr=yerr,
            label=label,
            elinewidth=0.5,
            capsize=0,
            fmt=fmt,
            **kwargs
        )
        # ax.plot(
        #     x_axis,
        #     y_axis,
        #     fmt,
        #     label=label,
        #     **kwargs
        # )
        # ax.fill_between(
        #     x_axis,
        #     y_axis - y_err,
        #     y_axis + y_err,
        #     alpha=0.5
        # )


def create_ax(
    rows, cols,
    x_axis,
    ys,
    xlabel,
    ylabel,
    labels,
    stacked
):
    fig, ax = plt.subplots(
        rows,
        cols,
        sharex=stacked
    )

    xlabel = set_if_none(xlabel, x_axis.name)

    if stacked:
        ax[-1].set(
            xlabel=xlabel,
        )

        ylabels = set_if_none(labels, [y.name for y in ys])

        for axis, ylabel in zip(ax, ylabels):
            axis.set(ylabel=ylabel)

    else:
        ax.set(xlabel=xlabel)

        if len(ys) == 1:
            ylabel = set_if_none(ylabel, ys[0].name)
            ax.set(
                ylabel=ylabel
            )

    return fig, ax


def data(
    df: pd.DataFrame,
    ax=None,
    label=None,
    fmt=None,
    xlabel=None,
    ylabel=None,
    labels=None,  # For multiple dependent variables
    stacked=False,
    **kwargs
):
    """Plot data from dataframe representing a function. The following
    structure is assumed:
     - 1st column is the independent variable,
     - 2nd is the uncertainty in the independent variable,
     - odd columns following are dependent variables,
     - even columns following are the uncertainty in the previous dependent
       variable.
    The 2nd column (X error) can be empty, but it has to be there.
    Pass `stacked=True` to draw each column in a separate row.
    """

    x_axis, xerr, ys, yerrs = split_axes(df)

    if len(ys) == 1:
        stacked = False

    # If there is no uncertainty in X, don't plot it
    xerr = xerr if not xerr.isna().all() else None

    fig = None

    rows = len(ys) if stacked else 1
    cols = 1

    # ax may be passed. If not, create a new figure
    if ax is None:
        fig, ax = create_ax(
            rows,
            cols,
            x_axis,
            ys,
            xlabel,
            ylabel,
            labels,
            stacked
        )

    # If no fmt is passed, it may be '-' or '.' depending on the number of
    # points
    fmt = set_if_none(fmt, fmt_choice(x_axis.size))

    if stacked:
        stack_plot(
            ax,
            x_axis,
            ys,
            xerr,
            yerrs,
            fmt,
            **kwargs
        )

    else:
        combine_plot(
            ax,
            x_axis,
            ys,
            xerr,
            yerrs,
            fmt,
            labels,
            **kwargs
        )

        plt.legend()

    return fig, ax


def combine_plot(
    ax,
    x_axis,
    ys,
    xerr,
    yerrs,
    fmt,
    labels,
    **kwargs
):
    # If passed, ax shuold have the right dimension
    if axis_bad_type(ax):
        logger.error("Invalid axis argument.")

        return None, None

    if len(ys) == 1:
        labels = [None]

    else:
        labels = set_if_none(labels, [y.name for y in ys])

    for y_axis, yerr, label in zip(ys, yerrs, labels):
        _plot(
            ax,
            x_axis,
            y_axis,
            xerr,
            yerr,
            fmt,
            label=label,
            **kwargs
        )

    return ax


def stack_plot(
    ax,
    x_axis,
    y_axes,
    xerr,
    yerrs,
    fmt,
    **kwargs
):
    # If passed, ax shuold have the right dimension
    if axes_bad_type(ax, n=len(y_axes)):
        logger.error(
            f"Invalid axes argument. Expected list of {len(y_axes)} axes."
        )

        return None

    for axis, y_axis, yerr in zip(ax, y_axes, yerrs):
        _plot(
            axis,
            x_axis,
            y_axis,
            xerr,
            yerr,
            fmt,
            label=None,
            **kwargs
        )

    return ax
