import logging
from . import _typing

logger = logging.getLogger("pylabo.plot")


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
        return None


def axis_basic_settings(
    ax,
    xlabel,
    ylabel,
    label
):
    ax.set(
        xlabel=xlabel,
        ylabel=ylabel
    )

    ax.grid(True)

    if label is not None:
        ax.legend()


def plot_errorbar(
    ax,
    x_data,
    y_data,
    xerr,
    yerr,
    fmt,
    label,
    xlabel,
    ylabel
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

    axis_basic_settings(ax, xlabel, ylabel, label)


def plot_smooth(
    ax,
    x_data,
    y_data,
    xerr,
    yerr,
    fmt,
    label,
    xlabel,
    ylabel
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

    axis_basic_settings(ax, xlabel, ylabel, label)


plot_functions = {
    "errorbar": plot_errorbar,
    "smooth": plot_smooth,
}
