import numpy as np
import scipy.stats


# reduced chi-squared
def chi2_r(
    residue,
    yerr,
    n_data,
    n_params
):
    chi2 = np.sum((residue / yerr) ** 2)
    degrees_of_freedom = n_data - n_params

    return chi2 / degrees_of_freedom


# R squared
def r2(
    y_data,
    residue
):
    return 1 - np.var(residue) / np.var(y_data)


def p_value(
    residue,
    yerr,
    n_data,
    n_params
):
    chi2 = np.sum((residue / yerr) ** 2)
    degrees_of_freedom = n_data - n_params

    return scipy.stats.chi2.sf(chi2, df=degrees_of_freedom)


# class Tests:
#     def __init__(
#         self,
#         y_data,
#         residue,
#         n_params
#     ):
