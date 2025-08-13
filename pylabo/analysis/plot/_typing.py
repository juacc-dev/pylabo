from numpy._typing import ArrayLike
from pandas.core.series import Series
from matplotlib.figure import Figure
from typing import Any
from pathlib import Path

# import matplotlib.pyplot as plt
# from . _helper import set_if_none
# from . _opts import opts


# class PylaboFigure:
#     def __init__(
#         self,
#         figsize=None,
#         dpi=None,
#         **kwargs
#     ):

#         self.figsize = set_if_none(figsize, opts.figsize)
#         self.dpi = set_if_none(dpi, opts.dpi)

#         self.figure: Figure = plt.figure(
#             figsize=self.figsize,
#             dpi=self.dpi,
#             **kwargs
#         )
