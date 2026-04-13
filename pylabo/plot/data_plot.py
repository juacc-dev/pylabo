import pandas as pd
import matplotlib.pyplot as plt
import logging

from pylabo.proc.dataframe import interpret
from pylabo.lib.utils import set_if_none
from pylabo.plot.utils import axis_bad_type, fmt_choice

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


def set_labels(
    ax,
    rows, cols,
    x_axis,
    ys,
    xlabel,
    ylabel,
    labels,
    stacked
):
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


def data(
    df: pd.DataFrame,
    ax=None,
    fmt=None,
    xlabel=None,
    ylabel=None,
    labels=None,  # For multiple dependent variables
    label=None,
    stacked=False,
    shape=(1, None),
    no_yerr=False,
    force_label=True,
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

    passed_ax = ax is not None

    x_axes, x_errs, y_axes, y_errs = interpret(df, shape=shape)

    x_axis = x_axes[0]
    xerr = x_errs[0]

    if len(y_axes) == 1:
        stacked = False

    # If there is no uncertainty in X, don't plot it
    xerr = xerr if not xerr.isna().all() else None

    fig = None

    rows = len(y_axes) if stacked else 1
    cols = 1

    # ax may be passed. If not, create a new figure
    if not passed_ax:
        fig, ax = plt.subplots(
            rows,
            cols,
            sharex=stacked
        )

    if not passed_ax or force_label:
        set_labels(
            ax,
            rows,
            cols,
            x_axis,
            y_axes,
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
            y_axes,
            xerr,
            y_errs,
            fmt,
            **kwargs
        )

    else:
        if len(y_axes) == 1:
            # `labels` is expected to be None if no labels were provided.
            # When plotting single Y axis, if `label` was set, then it should
            # be passed as `[label]`. If not set, nothing should be passed.
            labels = None if label is None else [label]

        combine_plot(
            ax,
            x_axis,
            y_axes,
            xerr,
            y_errs,
            fmt,
            labels,
            no_yerr,
            **kwargs
        )

        if fig is not None:
            plt.legend()

    return fig, ax


def combine_plot(
    ax,
    x_axis,
    y_axes,
    xerr,
    yerrs,
    fmt,
    labels,
    no_yerr,
    **kwargs
):
    # If passed, ax shuold have the right dimension
    if axis_bad_type(ax):
        logger.error("Invalid axis argument.")

        return None, None

    labels = set_if_none(labels, [y.name for y in y_axes])

    for y_axis, yerr, label in zip(y_axes, yerrs, labels):
        if no_yerr:
            yerr = None

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
    if axis_bad_type(ax, n=len(y_axes)):
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
