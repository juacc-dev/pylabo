import matplotlib.pyplot as plt

from pylabo.utils import set_if_none
import logging
from . _opts import opts
from . _helper import plot_functions, data_name
from . _typing import Any, Figure

logger = logging.getLogger("pylabo.plot")

def data(
    x_data: Any,
    y_data: Any | tuple[Any],
    error: Any | tuple[Any] = 0,
    xlabel: str = None,
    ylabel: str = None,
    label: str | list[str] = None,

    # saveto: str = None,    # custom save path
    separate_rows=False,    # use a different row for each plot if provided
    plot_method: str = None,
    xlim: tuple[Any] = None,
    ylim: tuple[Any] = None,

    fmt=None,
    figsize=None,
    **kwargs
) -> tuple[Figure, Any]:
    """
    Plot data with errors. Accepts multiple `y_data` asociated with the same
    `x_data` (i.e. multiple sets of data), if that is the case, either all sets
    of data will be plotted together or each one will be in a separate row.
    `error` can be either the error in `y_data` or a tuple containing
    the errors in `x_data` and `y_data`, i.e. `(x_err, y_err)`. If `y_data` is a
    list of y_datas, `y_err` shuold be a list as well.
    """

    fmt = set_if_none(fmt, opts.fmt)
    figsize = set_if_none(figsize, opts.figsize)
    xlabel = set_if_none(xlabel, data_name(x_data))
    ylabel = set_if_none(ylabel, data_name(y_data))

    if xlabel is None and ylabel is None:
        logger.warning("No axis labels specified for plot")

    # There may be multiple y_data
    multiplot = False if not isinstance(y_data, tuple) else len(y_data)

    if multiplot:
        logger.info(f"Doing multiple plots, y_data is of lenght {len(y_data)}.")

    if not multiplot and separate_rows:
        logger.warning(
            "Specified separate rows but there is only one set of data."
        )

    # if specified separate_rows, plot
    rows = 1 if not multiplot or not separate_rows else multiplot
    cols = 1
    logger.info(f"Plotting {rows} rows and {cols} columns.")

    fig, ax = plt.subplots(
        rows,
        cols,
        figsize=figsize,
        sharex=False if rows == 1 else True
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
                x_data,
                y_data,
                xerr,
                yerr,
                fmt,
                label,
                xlabel,
                ylabel
            )

        # There are multiple y_data, plot them together
        else:
            logger.info(f"Plotting {len(y_data)} sets of data.")

            for i in range(multiplot):
                lab = label[i] if isinstance(label, list) else label

                plot_function(
                    ax,
                    x_data,
                    y_data[i],
                    xerr,
                    yerr[i],
                    fmt,
                    lab,
                    xlabel,
                    ylabel
                )

    # There may be multiple y_data, plot them in separate rows
    else:
        logger.info(f"Plotting {rows} rows.")

        for i in range(rows):
            plot_function(
                ax[i],
                x_data,
                y_data[i],
                xerr,
                yerr[i],
                fmt,
                label,
                xlabel,
                ylabel
            )

    return fig, ax


def elements(
    x_data,
    y_data,
    error=None,
    *,
    xlabel: str = None,
    ylabel: str = None,
    fmt=None,
    figsize=None,
):
    fmt = set_if_none(fmt, opts.fmt)
    figsize = set_if_none(figsize, opts.figsize)
    xlabel = set_if_none(xlabel, data_name(x_data))
    ylabel = set_if_none(ylabel, data_name(y_data))

    rows = 2
    cols = 1

    fig, (ax_y, ax_x) = plt.subplots(
        rows,
        cols,
        figsize=figsize,
        sharex=True
    )

    (xerr, yerr) = error if isinstance(error, tuple) else (None, error)

    ax_x.plot(
        x_data,
        fmt
    )

    ax_x.set(
        xlabel="Número de elemento",
        ylabel=xlabel
    )

    ax_y.plot(
        y_data,
        fmt,
        label=ylabel
    )
    ax_y.set(
        ylabel=ylabel
    )

# def data_polar(
#     theta_data,
#     r_data,
#     rerr=None,
#     terr=None,
#     title: str = None,
#     label: str = None,
#     figsize=None,
#     fmt=None,
#     rorigin=None,
#     rlabel=None,
#     **kwargs
# ):
#     """
#     Plot data in polar coordinates.
#     """
#     fmt = set_if_none(fmt, opts.fmt)
#     figsize = set_if_none(figsize, opts.figsize)

#     fig, ax = plt.subplots(
#         figsize=figsize,
#         subplot_kw={'projection': 'polar'},
#         *kwargs
#     )

#     ax.errorbar(
#         theta_data,
#         r_data,
#         xerr=terr,
#         yerr=rerr,
#         fmt=fmt,
#         label=label
#     )

#     ax.set_thetamin(np.min(theta_data * 180 / np.pi))
#     ax.set_thetamax(np.max(theta_data * 180 / np.pi))
#     ax.set(ylabel=rlabel)

#     if rorigin is not None:
#         ax.set_rorigin(rorigin)

#     if label is not None:
#         ax.legend()

#     return
