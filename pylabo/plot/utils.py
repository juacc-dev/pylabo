from pylabo.plot.default_opts import opts


def fmt_choice(n_points: int):
    if n_points < opts.fmt_n_points:
        return "o"

    else:
        return "."


def axis_setup(
    ax,
    xlabel=None,
    ylabel=None,
):
    ax.grid(True)
    ax.legend()
    ax.set(
        xlabel=xlabel,
        ylabel=ylabel
    )
