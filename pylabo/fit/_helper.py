from scipy.optimize import curve_fit
import numpy as np
import pprint
import sys
import logging

from . import function

logger = logging.getLogger(__name__)

opt_show_result = False

def find(
    func: function.Function,
    data_x,
    data_y,
    p0=None,
    yerr=None
):
    """
    Fit a function to data.
    """

    try:
        param_opt, param_cov = curve_fit(
            func.f,
            data_x,
            data_y,
            p0=p0,
            sigma=yerr,
            absolute_sigma=True
        )
    except RuntimeError as e:
        logger.error("Failed to fit function :(.")
        logger.error(e)
        sys.exit(1)

    # Error in parameters
    param_err = np.sqrt(np.diag(param_cov))

    return param_opt, param_err


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
    residuos
):
    return 1 - np.var(residuos) / np.var(y_data)


def result(
    func: function.Function,
    p_opt,
    p_err,
    chi,
    r_sq
) -> list[dict]:
    # Fit statistics
    stats = {
        "Chi^2 red": f"{chi}",
        "R^2": f"{r_sq}",
    } if chi is not None else {
        "R^2": f"{r_sq}",
    }

    # Mean and error of parameters
    # "avg+-err" notation, it is very easy to parse later
    params = {
        p: f"{opt}+-{err}"
        for p, opt, err
        in zip(func.params, p_opt, p_err)
    }

    # Bundle into one dictionary
    res: dict = stats
    res.update(params)

    if opt_show_result:
        pprint.pp(res)

    return [res]
