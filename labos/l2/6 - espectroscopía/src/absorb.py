from common import data, plot, fit
import numpy as np
# import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


concentrations = [20, 40, 60, 80, 100]
PASO_OPTICO = 0.0128
ERROR = 0.025


def main(args) -> None:
    df_0 = data.find(file="lambda/0.csv")

    wl_0 = df_0.iloc[:, 0]
    i_0 = df_0.iloc[:, 1]

    wl = 0

    interpolator = interp1d(wl_0, i_0, kind='linear', fill_value="extrapolate")

    absorb = []
    absorb_err = []

    for conc in concentrations:
        df = data.find(file=f"lambda/{conc}.csv")
        wl = df.iloc[:, 0]
        i = df.iloc[:, 1]

        i_intp = interpolator(wl)

        abs = -np.log10(i / i_intp) / PASO_OPTICO
        absorb.append(abs)

        # Indirect error
        abs_err = ERROR * (i + i_intp) / (np.log(10) * i * i_intp * PASO_OPTICO)
        absorb_err.append(abs_err)

    # Each element is the absorbance as a function of concentration for each
    # value of lambda
    wavelengths = np.transpose(absorb)
    wavelengths_err = np.transpose(absorb_err)

    abs_mol = []
    abs_mol_err = []
    r2 = []
    chi2r = []

    # This is like looping over level sets lambda = lambda_0
    for absorbance, absorbance_err in zip(wavelengths, wavelengths_err):
        fit_func = fit.utils.fitnsave(
            fit.f.linear_homog,
            np.array(concentrations),
            np.array(absorbance),
            yerr=absorbance_err,
            nosave=True
        )

        abs_mol.append(fit_func.params[0])
        abs_mol_err.append(fit_func.p_err[0])
        r2.append(fit_func.r_sq)
        chi2r.append(fit_func.chi_sq_red)

    plot.data(
        wl,
        np.array(abs_mol),
        np.array(abs_mol_err),
        xlabel="Longitud de onda [nm]",
        ylabel=r"absortividad relativa [1/m$^2$]",
        saveto="absortividad"
    )

    plot.data(
        wl,
        np.array(r2),
        xlabel="Longitud de onda [nm]",
        ylabel=r"$R^2$",
        ylim=(-3, 1.1),
        saveto="absortividad-r2"
    )

    plot.data(
        wl,
        np.array(chi2r),
        xlabel="Longitud de onda [nm]",
        ylabel=r"$\chi^2_\nu$",
        ylim=(0, 6),
        saveto="absortividad-chi2_red"
    )
