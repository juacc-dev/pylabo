import numpy as np
import matplotlib.pyplot as plt
import logging

from pylabo import fit
from pylabo.utils import set_if_none
from . _helper import get_units, data_name
from . _opts import opts
from . _typing import Any
from . _data_plot import data
from . _save import save

logger = logging.getLogger("pylabo.plot")

def data_and_fit(
    x_data: Any,
    y_data: Any,
    error: Any | tuple[Any],
    fit_fun: fit.funs.EvalFunction,
    fmt=None,
    figsize=None,
    datalabel: str = "Mediciones",
    fitlabel: str = "Ajuste",
    xlabel: str = None,
    ylabel: str = None,
    units: float = None,
    residue_units: tuple[float, str] = None,
    noshow=False,
    saveto: str = None,
    **kwargs
):
    """
    Plot data, fit and residue. Works similar to `plot.data()` except that
    `y_data` may only contain a single array of data.

    Shows plots.
    """

    fmt = set_if_none(fmt, opts.fmt)
    figsize = set_if_none(figsize, opts.figsize)
    xlabel = set_if_none(xlabel, data_name(x_data))
    ylabel = set_if_none(ylabel, data_name(y_data))

    # If function is linear, use only 2 points for y_fit
    if fit_fun.func is fit.funs.linear:
        x_fit = np.array([min(x_data), max(x_data)])

    # else, create a higher resolution y_fit
    else:
        # Number of points depends on plot width
        n_points = figsize[0] * opts.dpi
        logger.info(f"Using {n_points} points to plot fit.")

        x_fit = np.linspace(min(x_data), max(x_data), n_points)

    y_fit = fit_fun.func.f(x_fit, *fit_fun.params)

    (x_units, y_units) = units if isinstance(units, tuple) else (None, units)
    (xerr, yerr) = error if isinstance(error, tuple) else (None, error)

    if y_units is not None:
        if ylabel is None:
            logger.warning("Did not change ylabel to accomodate for units.")

        y_data *= y_units
        y_fit *= y_units
        if yerr is not None:
            yerr *= y_units

    if x_units is not None:
        if xlabel is None:
            logger.warning("Did not change xlabel to accomodate for units.")

        x_data *= x_units
        x_fit *= x_units
        if xerr is not None:
            xerr *= x_units

    error = (xerr, yerr)

    fig, ax = data(
        x_data,
        y_data,
        error,
        noshow=True,
        label=datalabel,
        xlabel=xlabel,
        ylabel=ylabel,
        fmt=fmt,
        figsize=figsize,
        **kwargs,
    )

    # Plot fit in 'ax' (on top of the data)
    ax.plot(
        x_fit,
        y_fit,
        label=fitlabel
    )

    if fitlabel is not None:
        ax.legend()

    if saveto is not None:
        save(saveto, append="fit")

    # Plot residue separately

    fig_res, ax_res = plt.subplots(
        figsize=figsize
    )

    yerr = error[1] if isinstance(error, tuple) else error

    if residue_units is None:
        # Use units from ylabel
        ylabel = f"Residuos {get_units(ylabel)}"

    else:
        # Change units for residue
        fit_fun.residue *= residue_units[0]
        yerr *= residue_units[0]

        ylabel = f"Residuos [{residue_units[1]}]"

    ax_res.errorbar(
        x_data,
        fit_fun.residue,
        yerr=yerr,
        fmt=fmt)

    ax_res.set(xlabel=xlabel)
    ax_res.set(ylabel=ylabel)

    ax_res.grid(True)

    ax_res.axhline(0, color="black")

    # Append '-residue' to path to save figure
    if saveto is not None:
        save(saveto, append="residue")

    return fig, ax
