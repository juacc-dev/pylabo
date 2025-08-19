import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import logging
from matplotlib.axes import Axes

import pylabo.fit

from pylabo.plot.core import split_axes
from pylabo.plot.utils import fmt_choice
from pylabo.lib.utils import set_if_none

logger = logging.getLogger("pylabo.plot")


def fit(
    fit_func: pylabo.fit.FittedFunction,
    fig=None,
    ax=None,
    fmt=None,
    label=None,
    **kwargs
):
    """
    Plot the fitted function.
    To plot the fit on top of the data, use stacked() or combined() first.
    """

    n_points = 8 * plt.rcParams["figure.dpi"]

    x_fit = np.linspace(*fit_func.xlim, n_points)
    y_fit = fit_func.f(x_fit, *fit_func.param_val)

    if fig is None and ax is None:
        fig, ax = plt.subplots(
            1,
            1,
            sharex=True
        )

    elif type(ax) is not Axes:
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
    no_xerr=False,
    fig=None,
    ax=None,
    fmt=None,
    label="Residuos",
    **kwargs
):

    x_axis, x_err, _, y_errs = split_axes(df, no_xerr=no_xerr)

    y_err = y_errs[y_errs.columns[0]]

    if fig is None and ax is None:
        fig, ax = plt.subplots(
            1,
            1,
            sharex=True
        )

    elif type(ax) is not Axes:
        logger.error("Invalid axes argument.")

        return None, None

    # fmt may be 'o' or '.' depending on the number of points
    fmt = set_if_none(fmt, fmt_choice(x_axis.size))

    ax.errorbar(
        x_axis,
        fit_func.residue,
        xerr=x_err,
        yerr=y_err,
        **kwargs
    )

    return fig, ax
