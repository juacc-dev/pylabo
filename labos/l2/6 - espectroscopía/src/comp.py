from common import data, plot
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

MIN0 = 400
MAX0 = 700

REF1 = 449
REF2 = 485


def parse_intval(args):
    if len(args) > 2:
        new_min, new_max = float(args[1]), float(args[2])
        print(f"Using interval [{new_min}; {new_max}]")
        return new_min, new_max

    else:
        return MIN0, MAX0


def closest(series, value):
    index = (series - value).abs().idxmin()
    return index


def px_to_wl_agua(px):
    # Pixel to wavelength conversion
    m = (485 - 449) / (412 - 387)
    px_0 = 387
    lambda_0 = 449

    return m * (px - px_0) + lambda_0


def main(args) -> None:
    MIN, MAX = parse_intval(args)

    # Referencia

    df_0 = data.find(file="referencia.csv", sep=";")

    wl_0 = df_0.iloc[:, 0]
    i_0 = df_0.iloc[:, 1]

    intval_0 = (closest(wl_0, MIN), closest(wl_0, MAX))
    i_0 = i_0[intval_0[0]:intval_0[1]]
    i_0 /= i_0.max()

    wl_0 = wl_0[intval_0[0]:intval_0[1]]

    # Agua

    df_agua = data.find(file="agua destilada.csv")

    px = df_agua.iloc[:, 0]
    wl = px_to_wl_agua(px)
    i = df_agua.iloc[:, 1]

    intval = (closest(wl, MIN), closest(wl, MAX))
    i = i[intval[0]:intval[1]]
    i /= i.max()

    wl = wl[intval[0]:intval[1]]

    # Intepolation

    interpolator = interp1d(wl_0, i_0, kind='linear', fill_value="extrapolate")

    i_0 = interpolator(wl)

    # Plot
    plt.figure(figsize=(8, 6))

    plt.plot(wl, i_0, label="Referencia")
    plt.plot(wl, i, label="Cámara")

    plt.xlabel("Longitud de onda [nm]"),
    plt.ylabel("Intensidad"),

    plt.axvline(REF1, color="black", alpha=0.5)
    plt.axvline(REF2, color="black", alpha=0.5)

    plt.grid()
    plt.legend()

    plot.save(filename="comparación")
