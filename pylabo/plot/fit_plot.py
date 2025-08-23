import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import logging

import pylabo.fit
from pylabo.lib.split_axes import split_single
from pylabo.lib.utils import set_if_none
from pylabo.plot.data_plot import data
from pylabo.plot.utils import axis_is_bad, axes_are_bad, fmt_choice, axis_setup

logger = logging.getLogger("pylabo.plot")


def fitted(
    df: pd.DataFrame,
    fit_func: pylabo.fit.FittedFunction,
    ax=None,
    label=None,
    fmt=None,
    **kwargs
):
    """
    Plot the fitted function. More points are used as to draw a smooth curve.
    """
    x_axis, _, _, _ = split_single(df)

    n_points = int(8 * plt.rcParams["figure.dpi"])

    x_fit = np.linspace(x_axis.min(), x_axis.max(), n_points)
    y_fit = fit_func.f(x_fit, *fit_func.param_val)

    fig = None

    if ax is None:
        fig, ax = plt.subplots(
            1,
            1,
        )

    elif axis_is_bad(ax):
        logger.error("Invalid axes argument.")

        return None, None

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
    **kwargs
):
    """Plot the residue from a fit."""

    x_axis, x_err, _, y_err = split_single(df)

    fig = None

    if ax is None:
        fig, ax = plt.subplots(
            1,
            1,
        )

        axis_setup(
            ax,
            xlabel=x_axis.name,
            ylabel=ylabel
        )

    elif axis_is_bad(ax):
        logger.error("Invalid axes argument.")

        return None, None

    # fmt may be 'o' or '.' depending on the number of points
    fmt = set_if_none(fmt, fmt_choice(x_axis.size))
    ylabel = set_if_none(ylabel, "Residuos")

    # If there is no uncertainty in X, don't plot it
    x_err = x_err if not x_err.isna().all() else None

    ax.errorbar(
        x_axis,
        fit_func.residue,
        xerr=x_err,
        yerr=y_err,
        **kwargs
    )

    return fig, ax


def fulfit(
    df: pd.DataFrame,
    fit_func: pylabo.fit.FittedFunction,
    ax=None,
    fmt=None,
    datalabel=None,
    fitlabel=None,
    height_ratios=[3, 1]
):
    """Plot dataframe, fitted function and residue."""

    x_axis, _, y_axis, _ = split_single(df)

    fig = None

    if ax is None:
        fig, ax = plt.subplots(
            2,
            1,
            sharex=True,
            height_ratios=height_ratios
        )

        axis_setup(
            ax[0],
            ylabel=y_axis.name
        )
        axis_setup(
            ax[1],
            xlabel=x_axis.name,
            ylabel="Residuos"
        )

    elif axes_are_bad(ax, n=2):
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
        label=set_if_none(fitlabel, set_if_none(fit_func.eq, "Ajuste"))
    )

    ax[0].legend()

    residue(
        df,
        fit_func,
        ax=ax[1],
        fmt=fmt
    )

    return fig, ax
