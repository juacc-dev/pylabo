import logging
from . import _typing

logger = logging.getLogger(__name__)

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
