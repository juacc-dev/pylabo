import matplotlib.pyplot as plt
from pylabo.lib.opts import Options

opts = Options()
opts.fmt_n_points = 200

def setup_matplotlib():
    # plt.rcParams["mathtext.fontset"] = "cm"
    # plt.rcParams["font.family"] = "STIXGeneral"
    plt.rcParams["figure.dpi"] = 100
    # plt.rcParams["savefig.dpi"] = 100
    plt.rcParams["axes.grid"] = True
    plt.rcParams["font.family"] = "Noto Serif"
    plt.rcParams["figure.figsize"] = (9, 7)
    plt.rcParams["legend.fontsize"] = 11
    plt.rcParams["legend.loc"] = "best"
    plt.rcParams["legend.fontsize"] = 11  # 14
