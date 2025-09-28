from pylabo.plot.default_opts import opts
from matplotlib.axes import Axes


def axis_bad_type(ax):
    return type(ax) is not Axes


def axes_bad_type(ax, n=1):
    return type(ax[0]) is not Axes or len(ax) != n


def fmt_choice(n_points: int):
    if n_points < opts.fmt_n_points:
        return "."

    else:
        return "-"
