from . _utils import data_name
import logging

logger = logging.getLogger(__name__)

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

