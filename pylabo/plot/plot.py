import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from pylabo import fit, logging
from pylabo.utils import set_if_none
from pylabo._plot import _typing
# from pylabo._plot._helper import data_name, get_units, plot_errorbar, plot_smooth


logger = logging.init("pylabo.plot")



def plot():
