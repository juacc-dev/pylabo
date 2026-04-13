import matplotlib.pyplot as plt
from pylabo.lib.opts import Options

opts = Options()
opts.fmt_n_points = 200

def setup():
    plt.rcParams["mathtext.fontset"] = "cm"
    plt.rcParams["figure.dpi"] = 100
    # plt.rcParams["savefig.dpi"] = 100
    plt.rcParams["axes.grid"] = True
    plt.rcParams["font.family"] = "STIXGeneral"
    plt.rcParams["font.size"] = 14
    plt.rcParams["figure.figsize"] = (9, 7)
    plt.rcParams["legend.loc"] = "best"
