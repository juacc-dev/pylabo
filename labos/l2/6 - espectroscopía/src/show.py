from common import data, plot
import pandas as pd
import matplotlib.pyplot as plt

MIN0 = 400
MAX0 = 700


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


def px_to_wl(px):
    # Pixel to wavelength conversion
    m = (485 - 449) / (416 - 387)
    px_0 = 387
    lambda_0 = 449

    return m * (px - px_0) + lambda_0


def save_csv(file, x, y):
    df = pd.DataFrame({
        "Longitud de onda [nm]": x,
        "Intensidad relativa [%]": y
    })

    df.to_csv(f"data/lambda/{file}.csv", index=False)


def main(args) -> None:
    # df_ref = data.find(file="referencia.csv", sep=";")

    # plot.data(
    #     df_ref.iloc[:, 0],
    #     df_ref.iloc[:, 1],
    #     plot_method="smooth",
    #     saveto="referencia"
    # )
    MIN, MAX = parse_intval(args)

    df_agua = data.find(file="agua destilada.csv")

    px = df_agua.iloc[:, 0]
    wavelen = px_to_wl_agua(px)
    inten = df_agua.iloc[:, 1]

    intval = (closest(wavelen, MIN), closest(wavelen, MAX))
    peak = inten[intval[0]:intval[1]].max()

    wavelen = wavelen[intval[0]:intval[1]]
    inten = inten[intval[0]:intval[1]] / peak

    save_csv("0", wavelen, inten)

    if plot.opt_show_plots:
        plt.figure(figsize=(10, 8))

        plt.plot(
            wavelen,
            inten,
            label="Agua destilada"
        )
        # plot.data(
        #     wavelen,
        #     inten,
        #     xlabel="Longitud de onda [nm]",
        #     ylabel="Intensidad relativa [%]",
        #     plot_method="smooth",
        #     saveto="R0"
        # )

    for conc in ["20", "40", "60", "80", "100"]:
        df = data.find(file=f"rojo/R{conc}.csv")
        px = df.iloc[:, 0]
        wavelen = px_to_wl(px)

        inten = df.iloc[:, 1]

        intval = (closest(wavelen, MIN), closest(wavelen, MAX))

        wavelen = wavelen[intval[0]:intval[1]]
        inten = inten[intval[0]:intval[1]] / peak

        save_csv(conc, wavelen, inten)

        if plot.opt_show_plots:
            plt.plot(
                wavelen,
                inten,
                label=f"{conc}%"
            )
            # plot.data(
            #     wavelen,
            #     inten,
            #     xlabel="Longitud de onda [nm]",
            #     ylabel="Intensidad relativa [%]",
            #     plot_method="smooth",
            #     saveto=f"R{conc}"
            # )

    if plot.opt_show_plots:
        plt.grid()
        plt.legend()
        plt.xlabel("Longitud de onda [nm]")
        plt.ylabel("Intensidad")

        plot.save(filename="relative")
