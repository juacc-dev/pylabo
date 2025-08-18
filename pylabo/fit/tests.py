import numpy as np


# reduced chi-squared
def chi2_r(
    residue,
    y_err,
    n_data,
    n_params
):
    return np.sum((residue / y_err) ** 2) / (n_data - n_params)


# R squared
def r2(
    y_data,
    residue
):
    return 1 - np.var(residue) / np.var(y_data)
