"""Figures for chapter 5 (microstates of four molecules). Usage: python3 scripts/make_figures_ch5.py img"""
import sys
from itertools import combinations
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
from figstyle import save, PURPLE

out = sys.argv[1] if len(sys.argv) > 1 else "img"
MOL = "abcd"
COL = {"a": "tab:blue", "b": "tab:orange", "c": "tab:green", "d": "tab:red"}
W, H, GAP = 1.6, 0.9, 0.25            # box size and spacing
SLOTS = [(0.28, 0.28), (0.72, 0.28), (0.28, 0.72), (0.72, 0.72)]   # positions inside a half (fractions)

fig, ax = plt.subplots(figsize=(12, 6.6))
ax.set_aspect("equal"); ax.axis("off")
xmax = 6 * W + 5 * GAP
for row, nl in enumerate([4, 3, 2, 1, 0]):
    y = -row * (H + 0.45)
    micro = list(combinations(MOL, nl))
    n = len(micro)
    x0 = (xmax - (n * W + (n - 1) * GAP)) / 2
    if nl == 2:   # highlight the most probable macrostate
        ax.add_patch(FancyBboxPatch((x0 - 0.15, y - 0.15), n * W + (n - 1) * GAP + 0.3, H + 0.3,
                                    boxstyle="round,pad=0.02,rounding_size=0.15", fc="#efe6f7", ec=PURPLE, lw=1.2, zorder=0))
    for k, left in enumerate(micro):
        x = x0 + k * (W + GAP)
        ax.add_patch(Rectangle((x, y), W, H, fc="white", ec="0.25", lw=1.5, zorder=1))
        ax.plot([x + W / 2] * 2, [y + 0.04, y + H - 0.04], color="0.5", lw=1, ls="--", zorder=1)
        for i, m in enumerate(MOL):
            side = 0 if m in left else 1
            fx, fy = SLOTS[i]
            cx, cy = x + side * W / 2 + fx * W / 2, y + fy * H
            ax.add_patch(Circle((cx, cy), 0.15, fc=COL[m], ec="k", lw=0.8, zorder=2))
            ax.text(cx, cy - 0.005, m, ha="center", va="center", fontsize=10, color="white", fontweight="bold", zorder=3)
    ax.text(-0.4, y + H / 2, f"{nl} left", ha="right", va="center", fontsize=15)
    ax.text(xmax + 0.5, y + H / 2, rf"$\Omega={n}$", ha="left", va="center", fontsize=15,
            color=PURPLE if nl == 2 else "k")
    ax.text(xmax + 2.0, y + H / 2, f"{n}/16", ha="left", va="center", fontsize=14, color="0.35")
ax.text(-0.4, H + 0.35, "macrostate", ha="right", fontsize=14, color="0.35")
ax.text(xmax / 2, H + 0.35, "microstates (left half | right half)", ha="center", fontsize=14, color="0.35")
ax.text(xmax + 0.5, H + 0.35, r"$\Omega$", ha="left", fontsize=14, color="0.35")
ax.text(xmax + 2.0, H + 0.35, "probability", ha="left", fontsize=14, color="0.35")
ax.set_xlim(-2.2, xmax + 3.4); ax.set_ylim(-4 * (H + 0.45) - 0.2, H + 0.8)
save(fig, f"{out}/ch5_microstates.png")
