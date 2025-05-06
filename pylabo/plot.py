from pylabo import utils, fit
import logging
import numpy as np
import matplotlib.pyplot as plt

from pylabo._plot import _typing
from pylabo._plot._helper import data_name, get_units, plot_errorbar, plot_smooth

# Types

PLOTS_DIR = "plots"
DEFAULT_EXT = "png"
DEFAULT_FIGSIZE = (8, 6)
DPI = 100
FONT_SIZE = 18
DEFAULT_FMT = "o"

logger = logging.getLogger(__name__)

opt_show_plots = False

plt.rcParams.update({"font.size": FONT_SIZE})

plot_functions = {
    "errorbar": plot_errorbar,
    "smooth": plot_smooth,
}

def save(
    filename: _typing.Path = None,
    append: str = None,
    **kwargs
):
    plt.tight_layout()

    # Default save location
    path, name = utils.get_caller_name()

    if filename is not None:
        name = filename

    stem = f"{name}.{DEFAULT_EXT}"

    filename = path / PLOTS_DIR / stem

    if append is not None:
        filename = filename.parent / \
            f"{filename.stem}-{append}{filename.suffix}"

    logger.info(f"Saving figure at '{filename}'.")
    plt.savefig(filename, **kwargs)

    if opt_show_plots:
        logger.info(f"Showing plot for '{filename.stem}'.")
        plt.show()

    plt.close()



def data(
    x_data: _typing.Any,
    y_data: _typing.Any | list[_typing.Any],
    error: _typing.Any | tuple[_typing.Any] = 0,
    label: str | list[str] = None,
    xlabel: str = None,
    ylabel: str = None,
    fmt=DEFAULT_FMT,
    figsize=DEFAULT_FIGSIZE,
    noshow=False,           # don't show the plot
    saveto: _typing.Path = None,    # custom save path
    separate_rows=False,    # use a different row for each plot if provided
    plot_method: str = None,
    xlim: tuple[_typing.Any] = None,
    ylim: tuple[_typing.Any] = None,
    **kwargs
) -> tuple[_typing.Figure, _typing.Any]:
    """
    Plot data with errors. Accepts multiple `y_data` asociated with the same
    `x_data` (i.e. multiple sets of data), if that is the case, either all sets
    of data will be plotted together or each one will be in a separate row.
    `error` can be either the error in `y_data` or a tuple containing
    the errors in `x_data` and `y_data`, i.e. `(x_err, y_err)`. If `y_data` is a
    list of y_datas, y_err shuold be a list as well.
    """

    # There may be multiple y_data
    multiplot = False if not isinstance(y_data, list) else len(y_data)

    if not multiplot and separate_rows:
        logger.warning(
            "Specified separate rows but there is only one set of data"
        )

    # if specified separate_rows, plot
    rows = 1 if not multiplot or not separate_rows else multiplot
    cols = 1

    fig, ax = plt.subplots(
        rows,
        cols,
        figsize=figsize,
        sharex=False if rows == 1 else True,
        **kwargs
    )

    # Change domain
    if xlim is not None:
        ax.set_xlim(xlim[0], xlim[1])

    if ylim is not None:
        ax.set_ylim(ylim[0], ylim[1])

    # error may be (x_err, y_err) or just y_err
    (xerr, yerr) = error if isinstance(error, tuple) else (None, error)

    if yerr is None:
        yerr = [0 for _ in range(multiplot)] if multiplot else 0

    if plot_method is None:
        plot_method = "errorbar" if len(x_data) < 100 else "smooth"
    plot_function = plot_functions[plot_method]

    # Simple plot for only one set of data
    if rows == 1:
        if not multiplot:
            logger.info("Plotting data.")

            plot_function(
                ax,
                x_data, y_data,
                xerr, yerr,
                fmt, label, xlabel, ylabel
            )

        # There are multiple y_data, plot them together
        else:
            logger.info(f"Plotting {len(y_data)} sets of data.")

            for i in range(multiplot):
                lab = label[i] if isinstance(label, list) else label

                plot_function(
                    ax,
                    x_data, y_data[i],
                    xerr, yerr[i],
                    fmt, lab, xlabel, ylabel
                )

    # There may be multiple y_data, plot them in separate rows
    else:
        logger.info(f"Plotting {rows} rows.")

        for i in range(rows):
            plot_function(
                ax[i],
                x_data, y_data[i],
                xerr, yerr[i],
                fmt, label, xlabel, ylabel
            )

    # noshow is useful if wanting to add something to the plot
    if not noshow:
        save(saveto)

    return fig, ax


def data_and_fit(
    x_data: _typing._typing.Any,
    y_data: _typing._typing.Any,
    error: _typing._typing.Any | tuple[_typing._typing.Any],
    fit_func: fit.f.EvalFunction,
    fmt=DEFAULT_FMT,
    figsize=DEFAULT_FIGSIZE,
    datalabel: str = "Mediciones",
    fitlabel: str = "Ajuste",
    xlabel: str = None,
    ylabel: str = None,
    units: float = None,
    residue_units: tuple[float, str] = None,
    noshow=False,
    saveto: _typing.Path = None,
    **kwargs
):
    """
    Plot data, fit and residue. Works similar to `plot.data()` except that
    `y_data` may only contain a single array of data.
    """

    if units is not None:
        if ylabel is None:
            logger.warning("Did not change ylabel to accomodate for units.")
        y_data *= units

    xlabel = xlabel if xlabel is not None else data_name(x_data)
    ylabel = ylabel if ylabel is not None else data_name(y_data)

    fig, ax = data(
        x_data,
        y_data,
        error,
        noshow=True,
        label=datalabel,
        xlabel=xlabel,
        ylabel=ylabel,
        fmt=fmt,
        **kwargs,
    )

    # If function is linear, use only 2 points for y_fit
    if fit_func.func is fit.f.linear:
        x_fit = np.array([min(x_data), max(x_data)])

    # else, create a higher resolution y_fit
    else:
        # Number of points depends on plot width
        n_points = DEFAULT_FIGSIZE[0] * DPI
        logger.info(f"Using {n_points} points to plot fit.")

        x_fit = np.linspace(min(x_data), max(x_data), n_points)

    y_fit = fit_func.func.f(x_fit, *fit_func.params)

    if units is not None:
        y_fit *= units

    # Plot fit in 'ax' (on top of the data)
    ax.plot(
        x_fit,
        y_fit,
        label=fitlabel
    )

    if fitlabel is not None:
        ax.legend()

    if not noshow:
        save(saveto, append="fit")

    # Plot residue separately

    fig_res, ax_res = plt.subplots(
        figsize=DEFAULT_FIGSIZE
    )

    yerr = error[1] if isinstance(error, tuple) else error

    if residue_units is None:
        # Use units from ylabel
        ylabel = f"Residuos {get_units(ylabel)}"

    else:
        # Change units for residue
        fit_func.residue *= residue_units[0]
        yerr *= residue_units[0]

        ylabel = f"Residuos [{residue_units[1]}]"

    ax_res.errorbar(
        x_data,
        fit_func.residue,
        yerr=yerr,
        fmt=fmt)

    ax_res.set(xlabel=xlabel)
    ax_res.set(ylabel=ylabel)

    ax_res.grid(True)

    ax_res.axhline(0, color="black")

    # Append '-residue' to path to save figure
    save(saveto, append="residue")

    return fig, ax


def data_polar(
    theta_data,
    r_data,
    rerr=None,
    terr=None,
    title: str = None,
    label: str = None,
    figsize=DEFAULT_FIGSIZE,
    rorigin=None,
    rlabel=None,
    fmt=DEFAULT_FMT,
    **kwargs
):
    """
    Plot data in polar coordinates.
    """

    fig, ax = plt.subplots(
        figsize=figsize,
        subplot_kw={'projection': 'polar'},
        *kwargs
    )

    ax.errorbar(
        theta_data,
        r_data,
        xerr=terr,
        yerr=rerr,
        fmt=fmt,
        label=label
    )

    ax.set_thetamin(np.min(theta_data * 180 / np.pi))
    ax.set_thetamax(np.max(theta_data * 180 / np.pi))
    ax.set(ylabel=rlabel)

    if rorigin is not None:
        ax.set_rorigin(rorigin)

    if label is not None:
        ax.legend()

    return
