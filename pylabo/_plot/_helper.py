from pylabo import logging
from . import _typing

logger = logging.init("pylabo.plot")

def get_units(label: str) -> str:
    """
    Extract units from a string.
    If `label` is "Weight [Kg]", the units are "[Kg]".
    """

    if label is None:
        return ""

    # Units are always at the end of a string
    units = label.split(" ")[-1]

    # Units are enclosed by "[]"
    if units[0] == '[' and units[-1] == ']':
        return units

    else:
        return ""


def data_name(data) -> str | None:
    if isinstance(data, _typing.Series):
        return data.name

    else:
        logger.warning("Label not specified")
        return None

def plot_errorbar(
    ax,
    x_data, y_data,
    xerr, yerr,
    fmt, label, xlabel, ylabel
):

    # Simple plot
    ax.errorbar(
        x_data,
        y_data,
        xerr=xerr,
        yerr=yerr,
        fmt=fmt,
        label=label
    )

    ax.set(xlabel=xlabel if xlabel is not None else data_name(x_data))
    ax.set(ylabel=ylabel if ylabel is not None else data_name(y_data))

    ax.grid(True)

    if label is not None:
        ax.legend()


def plot_smooth(
    ax,
    x_data, y_data,
    xerr, yerr,
    fmt, label, xlabel, ylabel
):
    # Simple plot
    ax.plot(
        x_data,
        y_data,
        label=label
    )

    ax.fill_between(
        x_data,
        y_data - yerr,
        y_data + yerr,
        color="green", alpha=0.2,
        label="Error"
    )

    ax.set(xlabel=xlabel if xlabel is not None else data_name(x_data))
    ax.set(ylabel=ylabel if ylabel is not None else data_name(y_data))

    ax.grid(True)

    if label is not None:
        ax.legend()
