import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import logging

import pylabo.fit
from pylabo.proc.dataframe import interpret
from pylabo.lib.utils import set_if_none
from pylabo.plot.data_plot import data
from pylabo.plot.utils import axis_bad_type

logger = logging.getLogger("pylabo.plot")


def fitted(
    df: pd.DataFrame,
    fit_func: pylabo.fit.FittedFunction,
    ax=None,
    label=None,
    **kwargs
):
    """
    Plot the fitted function. More points are used as to draw a smooth curve.
    """
    x_axes, _, _, _ = interpret(df, shape=(1, None))

    x_axis = x_axes[0]

    n_points = int(8 * plt.rcParams["figure.dpi"])

    x_fit = np.linspace(x_axis.min(), x_axis.max(), n_points)
    y_fit = fit_func.f(x_fit, *fit_func.param_val)

    fig = None

    if ax is None:
        fig, ax = plt.subplots(
            1,
            1,
        )

    elif axis_bad_type(ax):
        logger.error("Invalid axes argument.")

        return None, None

    label = set_if_none(label, set_if_none(fit_func.eq, "Ajuste"))

    ax.plot(
        x_fit,
        y_fit,
        label=label,
        **kwargs
    )

    return fig, ax


def residue(
    df: pd.DataFrame,
    fit_func: pylabo.fit.FittedFunction,
    ax=None,
    fmt=None,
    ylabel=None,
    label=None,
    no_yerr=False,
    **kwargs
):
    """Plot the residue from a fit."""

    x_axes, x_errs, _, y_errs = interpret(df, shape=(1, None))

    x_axis = x_axes[0]
    xerr = x_errs[0]
    yerr = y_errs[0]

    # ylabel = set_if_none(ylabel, "Residuos")

    # If there is no uncertainty in X, don't plot it
    xerr = xerr if not xerr.isna().all() else None

    if no_yerr:
        yerr = None

    ax.axhline(
        y=0,
        color="black",
        alpha=0.9
    )

    ax.errorbar(
        x_axis,
        fit_func.residue,
        xerr=xerr,
        yerr=yerr,
        fmt='.',
        label=label,
        **kwargs
    )

    return ax


def datafit(
    df: pd.DataFrame,
    fit_func: pylabo.fit.FittedFunction,
    ax=None,
    fmt=None,
    datalabel=None,
    fitlabel=None,
    reslabel=None,
    fit_color=None,
    data_color=None,
    height_ratios=[3, 1],
    no_yerr=False,
    force_label=True,
):
    """Plot dataframe, fitted function and residue."""

    passed_ax = ax is not None

    x_axes, _, y_axes, _ = interpret(df, shape=(1, None))
    x_axis = x_axes[0]
    y_axis = y_axes[0]

    fig = None

    if not passed_ax:
        fig, ax = plt.subplots(
            2,
            1,
            sharex=True,
            height_ratios=height_ratios
        )

    elif axis_bad_type(ax, n=2):
        logger.error("Invalid axes argument.")
        return None, None

    if not passed_ax or force_label:
        ax[0].set(
            ylabel=y_axis.name
        )
        ax[1].set(
            xlabel=x_axis.name,
            ylabel="Residuos"
        )

    data(
        df,
        ax=ax[0],
        fmt=fmt,
        label=datalabel,
        color=data_color,
        no_yerr=no_yerr,
        force_label=False
    )

    fitted(
        df,
        fit_func,
        ax=ax[0],
        label=fitlabel,
        color=fit_color
    )

    residue(
        df,
        fit_func,
        ax=ax[1],
        label=reslabel,
        color=data_color,
        no_yerr=no_yerr
    )

    if fig is not None:
        ax[0].legend()

        if reslabel is not None:
            ax[1].legend()

    return fig, ax
