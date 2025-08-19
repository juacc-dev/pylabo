from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
from pathlib import Path
import logging

from pylabo.fit.function import Function, FittedFunction
from pylabo.fit.tests import chi2_r, r2
from pylabo.fit.funs import linear, linear_homog

logger = logging.getLogger("pylabo.fit")


def fit_real(
    func: Function,
    data_x,
    data_y,
    p0=None,
    yerr=None
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
            absolute_sigma=True
        )

    except RuntimeError as e:
        logger.error(f"Failed to fit function. Error: {e}")
        return None, None

    # Error in parameters
    param_err = np.sqrt(np.diag(param_cov))

    return param_opt, param_err


def fit(
    func: Function,
    x_data,
    y_data,
    p0=None,
    yerr=None,
    saveto: Path | str = None,
) -> FittedFunction:
    """
    Fit a function to data.
    Returns an object containing all information about the result.
    """

    p_opt, p_err = fit_real(
        func,
        x_data,
        y_data,
        p0=p0,
        yerr=yerr
    )

    if p_opt is None and p_err is None:
        return None

    y_fit = func.f(x_data, *p_opt)

    residue = y_fit - y_data

    # Tests
    r_sq = r2(y_data, residue)
    chi = chi2_r(
        residue,
        yerr,
        len(residue),
        len(p_opt)
    )

    # New Function object
    fit_func = FittedFunction(
        func,
        p_opt,
        p_err,
        (x_data.min(), x_data.max()),
        residue,
        {
            "chi2r": chi,
            "R2": r_sq
        }
    )

    return fit_func


def report(
    fit_func: FittedFunction,
) -> pd.DataFrame:
    """Create a dataframe with the results of the fit: tests (like reduced chi
    squared) and optimal parameters with their uncertainty."""

    # 1st column: parameter names
    names = list(fit_func.tests.keys()) + fit_func.param_str

    # 2nd column: values / optimal values
    values = list(fit_func.tests.values()) + fit_func.param_val

    # 3rd column: uncertainty. Tests don't have any
    errors = [None for _ in range(len(fit_func.tests))] + fit_func.param_val

    df = pd.DataFrame({
        "Parámetro": pd.Series(names),
        "Valor": pd.Series(values),
        "Error": pd.Series(errors)
    })

    return df
