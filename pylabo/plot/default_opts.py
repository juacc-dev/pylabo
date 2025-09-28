import matplotlib.pyplot as plt
from pylabo.lib.opts import Options

plt.rcParams["figure.dpi"] = 100
# plt.rcParams["savefig.dpi"] = 100
plt.rcParams['axes.grid'] = True
plt.rcParams["font.family"] = "Noto Serif"
plt.rcParams["figure.figsize"] = (9, 7)
plt.rcParams['legend.loc'] = "best"
plt.rcParams['legend.fontsize'] = 11  # 14

opts = Options()
opts.fmt_n_points = 200
