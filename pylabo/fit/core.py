from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
import logging

from pylabo.fit.function import Function, FittedFunction
from pylabo.fit.tests import chi2_r, r2, p_value
from pylabo.fit.funs import linear, linear_homog
from pylabo.lib.split_axes import split_single

logger = logging.getLogger("pylabo.fit")


def fit_real(
    func: Function,
    data_x,
    data_y,
    p0=None,
    yerr=None,
    absolute_sigma=True
):
    """
    Fit a real function (wraped in the Function class) to data using curve_fit.
    """

    if p0 is None and not (func is linear or func is linear_homog):
        logger.warning(
            "Passing no initial parameters to nonlinear function."
        )

    try:
        param_opt, param_cov = curve_fit(
            func.f,
            data_x,
            data_y,
            p0=p0,
            sigma=yerr,
            absolute_sigma=absolute_sigma
        )

    except RuntimeError as e:
        logger.error(f"Failed to fit function. Error: {e}")
        return None, None

    return param_opt, param_cov


def fit(
    model: Function,
    df: pd.DataFrame,
    p0=None,
    absolute_sigma=True
) -> FittedFunction:
    """
    Fit a function to data.
    Returns an object containing all information about the result.
    """

    x_data, _, y_data, yerr = split_single(df)

    yerr = yerr if not yerr.isna().all() else None

    p_opt, p_cov = fit_real(
        model,
        x_data,
        y_data,
        p0=p0,
        yerr=yerr,
        absolute_sigma=absolute_sigma
    )

    if p_opt is None and p_cov is None:
        return None

    # Error in parameters
    p_err = np.sqrt(np.diag(p_cov))

    y_fit = model.f(x_data, *p_opt)

    residue = y_fit - y_data

    # Tests
    r_sq = r2(y_data, residue)
    chi = chi2_r(
        residue,
        yerr,
        len(residue),
        len(p_opt)
    ) if yerr is not None else None

    p_val = p_value(residue, yerr, len(residue), len(p_opt))

    # New Function object
    fit_func = FittedFunction(
        model,
        p_opt,
        p_cov,
        p_err,
        residue,
        tests={
            "R2": r_sq,
            "chi2 red": chi,
            "P value": p_val
        }
    )

    return fit_func
