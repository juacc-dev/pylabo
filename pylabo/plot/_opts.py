import logging
import matplotlib.pyplot as plt

logger = logging.getLogger("pylabo.plot")

DEFAULT_OPTS = {
    "font_family":  "TeX Gyre Schola:Regular",
    "font_size":    14,
    "dir":          "plots",
    "ext":          "png",
    "figsize":      (8, 6),
    "dpi":          100,
    "fmt":          "o",
    "layout":       "compressed",
}

def opts(**kwargs):
    for k, v in kwargs.items():
        if k in DEFAULT_OPTS:
            opts.k = v

            match k:
                case "font_family":
                    plt.rcParams["font.family"] = v

                case "font_size":
                    plt.rcParams["font.size"] = v

        else:
            logger.error("Invalid plot option.")
            return
