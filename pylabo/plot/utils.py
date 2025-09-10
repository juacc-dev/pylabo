from pylabo.plot.default_opts import opts
from matplotlib.axes import Axes


def axis_is_bad(ax):
    return type(ax) is not Axes


def axes_are_bad(ax, n=1):
    return type(ax[0]) is not Axes or len(ax) != n


def fmt_choice(n_points: int):
    if n_points < opts.fmt_n_points:
        return "."

    else:
        return "-"


def axis_setup(
    ax,
    xlabel=None,
    ylabel=None,
):
    ax.grid(True)
    ax.set(
        xlabel=xlabel,
        ylabel=ylabel
    )
