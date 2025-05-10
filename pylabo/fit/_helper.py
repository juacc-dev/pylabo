import numpy as np
import pprint

from . import funs

opt_show_result = False


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
    func: funs.Function,
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
