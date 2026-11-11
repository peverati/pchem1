"""Shared drawing of a "machine with knobs" (used in chapters 1 and 8).

Each knob carries its variable written on it, and each variable always has the same color.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 16})

VAR_COLORS = {"a": "tab:blue", "b": "tab:orange", "c": "tab:green",
              "S": "tab:blue", "T": "tab:red", "V": "tab:orange", "P": "tab:brown", "n": "tab:green"}


def draw_machine_ax(ax, x0, y0, s, display, knobs, title):
    """Draw a machine on an existing axis, with lower-left corner (x0, y0) and scale s.
    knobs: list of 3 tuples (variable key, math label, differential label)."""
    X = lambda x: x0 + s * x
    Y = lambda y: y0 + s * y
    ax.add_patch(FancyBboxPatch((X(1), Y(0.6)), 8 * s, 4.6 * s, boxstyle=f"round,pad={0.1*s},rounding_size={0.3*s}",
                                fc="#e8eef5", ec="#33475b", lw=2.5))
    ax.text(X(5), Y(5.6), title, ha="center", fontsize=15 * s ** 0.5, color="#33475b")
    ax.add_patch(FancyBboxPatch((X(3), Y(3.55)), 4 * s, 1.3 * s, boxstyle=f"round,pad={0.05*s},rounding_size={0.15*s}",
                                fc="#1f2b38", ec="#33475b", lw=2))
    ax.text(X(5), Y(4.2), display, ha="center", va="center", fontsize=24 * s ** 0.5, color="#7CFC9A", family="monospace")
    for x, (key, label, diff) in zip([2.6, 5, 7.4], knobs):
        c = VAR_COLORS[key]
        ax.add_patch(Circle((X(x), Y(1.65)), 0.72 * s, fc=c, ec="#33475b", lw=2))
        ax.plot([X(x + 0.42), X(x + 0.6)], [Y(2.07), Y(2.30)], color="white", lw=3 * s, solid_capstyle="round")
        ax.text(X(x), Y(1.6), label, ha="center", va="center", fontsize=21 * s ** 0.5, color="white", fontweight="bold")
        ax.add_patch(FancyArrowPatch((X(x - 0.85), Y(2.5)), (X(x + 0.85), Y(2.5)), connectionstyle="arc3,rad=-0.45",
                                     arrowstyle="-|>", mutation_scale=16 * s, lw=1.6, color=c))
        ax.text(X(x + 0.8), Y(2.65), diff, fontsize=15 * s ** 0.5, color=c, va="bottom")


def draw_machine(path, display, knobs, title="the machine"):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.4); ax.set_aspect("equal"); ax.axis("off")
    draw_machine_ax(ax, 0, 0, 1.0, display, knobs, title)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    print("saved", path)
