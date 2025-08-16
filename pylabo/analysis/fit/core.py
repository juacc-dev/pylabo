from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
from pathlib import Path
import logging

import pylabo.acquire.csv as csv
import pylabo.analysis.fit.funs as funs
from pylabo.analysis.fit.utils import chi2_r, r2, result

logger = logging.getLogger("pylabo.analysis.fit")


class Function:
    """
    Mathematical function with information about the parameters.
    """

    def __init__(
        self,
        f,               # Callable
        param_str: list[str],  # Parameter names
        eq: str = None      # LaTeX formula
    ):
        self.f = f
        self.params = param_str
        self.eq = eq


class FittedFunction(Function):
    """
    Function class together with numeric parameters and information about the
    fit.
    """

    def __init__(
        self,
        func: Function,
        param_val: list[float],
        param_err: list[float],
        residue,
        tests
    ):
        super().__init__(
            self,
            func.f,
            func.param_str,
            func.eq
        )
        self.params = param_val
        self.p_err = param_err
        self.residue = residue
        self.tests = tests


def fit_real(
    func: Function,
    data_x,
    data_y,
    p0=None,
    yerr=None
):
    """
    Fit a real functin (wraped in the Function class) to data using curve_fit.
    """

    if not (func is funs.linear or func is funs.linear_homog) and p0 is None:
        logger.warning(
            "No initial parameters passed to nonlinear function."
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
