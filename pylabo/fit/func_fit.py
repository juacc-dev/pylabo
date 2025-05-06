from pathlib import Path
from pylabo import data
import logging

from . import function
from . _helper import find, chi2_r, r2, result

logger = logging.getLogger(__name__)


def func_fit(
    func: function.Function,
    x_data,
    y_data,
    saveto: Path | str = None,
    p0=None,
    yerr=None,
    nosave=False
) -> function.EvalFunction:
    """
    Fit a function to data and save results.
    Returns y_fit and (param_opt, param_err)
    """

    if not (func is function.linear or func is function.linear_homog) \
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

    if not (func is function.linear or func is function.linear_homog):
        logger.warning("Non linear function. Calculating chi squared anyways.")

    # R^2 test
    r_sq = r2(y_data, residue)

    fit_func = function.EvalFunction(
        func,
        p_opt,
        p_err,
        residue,
        r_sq,
        chi_sq_red
    )

    if not nosave:
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
