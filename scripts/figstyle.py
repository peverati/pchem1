"""Common style for the computed figures of P-Chem 1 (same as P-Chem 2)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 16,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})

PURPLE = "tab:purple"


def save(fig, path):
    fig.savefig(path)
    plt.close(fig)
    print("saved", path)
