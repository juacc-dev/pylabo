import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import logging

import pylabo.fit
from pylabo.lib.utils import set_if_none, split_axes
from pylabo.plot.data_plot import data
from pylabo.plot.utils import axis_bad_type, axes_bad_type

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
    x_axis, _, _, _ = split_axes(df)

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
        label=label
    )

    return fig, ax


def residue(
    df: pd.DataFrame,
    fit_func: pylabo.fit.FittedFunction,
    ax=None,
    fmt=None,
    ylabel=None,
    # **kwargs
):
    """Plot the residue from a fit."""

    x_axis, xerr, _, yerrs = split_axes(df)
    yerr = yerrs[0]

    # ylabel = set_if_none(ylabel, "Residuos")

    # If there is no uncertainty in X, don't plot it
    xerr = xerr if not xerr.isna().all() else None

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
        # **kwargs
    )

    return ax


def datafit(
    df: pd.DataFrame,
    fit_func: pylabo.fit.FittedFunction,
    ax=None,
    fmt=None,
    datalabel=None,
    fitlabel=None,
    height_ratios=[3, 1]
):
    """Plot dataframe, fitted function and residue."""

    x_axis, _, ys, _ = split_axes(df)
    y_axis = ys[0]

    fig = None

    if ax is None:
        fig, ax = plt.subplots(
            2,
            1,
            sharex=True,
            height_ratios=height_ratios
        )

        ax[0].set(
            ylabel=y_axis.name
        )
        ax[1].set(
            xlabel=x_axis.name,
            ylabel="Residuos"
        )

    elif axes_bad_type(ax, n=2):
        logger.error("Invalid axes argument.")
        return None, None

    data(
        df,
        ax=ax[0],
        fmt=fmt,
        label=set_if_none(datalabel, "Mediciones")
    )

    fitted(
        df,
        fit_func,
        ax=ax[0],
        fmt=fmt,
        label=fitlabel
    )

    ax[0].legend()

    residue(
        df,
        fit_func,
        ax=ax[1],
    )

    return fig, ax
