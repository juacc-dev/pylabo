from pylabo.plot.config import opts
from matplotlib.axes import Axes


def axis_bad_type(ax, n=None):
    if n is not None:
        if type(ax) is list:
            return type(ax[0]) is not Axes or len(ax) != n
        else:
            return False

    return type(ax) is not Axes


def fmt_choice(n_points: int):
    if n_points < opts.fmt_n_points:
        return "."

    else:
        return "-"
