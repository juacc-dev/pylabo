from pylabo.plot.default_opts import opts


def fmt_choice(n_points: int):
    if n_points < opts.fmt_n_points:
        return "o"

    else:
        return "."
