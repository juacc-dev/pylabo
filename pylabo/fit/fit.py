from scipy.optimize import curve_fit
import numpy as np
from pathlib import Path
# import logging
import sys

from pylabo import data, logging
from . import funs
from . _helper import chi2_r, r2, result

logger = logging.init("pylabo.fit")


def find(
    func: funs.Function,
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
        logger.warning("Failed to fit function :(.")
        logger.warning(e)
        sys.exit(1)

    # Error in parameters
    param_err = np.sqrt(np.diag(param_cov))

    return param_opt, param_err


def func_fit(
    func: funs.Function,
    x_data,
    y_data,
    p0=None,
    yerr=None,
    saveto: Path | str = None,
) -> funs.EvalFunction:
    """
    Fit a function to data and save results.
    Returns y_fit and (param_opt, param_err)
    """

    if not (func is funs.linear or func is funs.linear_homog) \
            and p0 is None:
        logger.warning("Passing no initial parameters for non linear function.")

    p_opt, p_err = find(
        func,
        x_data,
        y_data,
        p0=p0,
        yerr=yerr
    )

    y_fit = func.f(x_data, *p_opt)

    residue = y_fit - y_data

    # Chi squared test is only relevant for lineal fits
    chi_sq_red = chi2_r(
        residue,
        yerr,
        len(residue),
        len(p_opt)
    )

    if not (func is funs.linear or func is funs.linear_homog):
        logger.warning("Non linear function. Calculating chi squared anyways.")

    # R^2 test
    r_sq = r2(y_data, residue)

    fit_func = funs.EvalFunction(
        func,
        p_opt,
        p_err,
        residue,
        r_sq,
        chi_sq_red
    )

    if saveto is not None:
        res = result(
            func,
            p_opt,
            p_err,
            chi_sq_red,
            r_sq
        )

        # Save result to disk
        data.save(res, filename=saveto)

    return fit_func
