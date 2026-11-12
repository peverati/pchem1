"""Figures for chapter 1. Usage (from the project root): python3 scripts/make_figures_ch1.py img"""
import sys
from machine import draw_machine

out = sys.argv[1] if len(sys.argv) > 1 else "img"
draw_machine(f"{out}/machine_knobs.png", r"$\mathcal{M}=\,$" + "42.0",
             [("a", "$a$", "$da$"), ("b", "$b$", "$db$"), ("c", "$c$", "$dc$")], title="")

# ---------- four examples of thermodynamic systems and their boundaries ----------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Circle
from figstyle import save

fig, axs = plt.subplots(1, 4, figsize=(14, 4.4))
for ax in axs:
    ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.set_aspect("equal"); ax.axis("off")
rng = np.random.default_rng(1)

# flask with a liquid: physical boundary (glass)
ax = axs[0]
flask = [(4, 10), (6, 10), (6, 7), (9, 1), (1, 1), (4, 7)]
ax.add_patch(Polygon([(4.15, 5.0), (5.85, 5.0), (8.6, 1.15), (1.4, 1.15)], fc="#7fd17f", ec="none"))
ax.add_patch(Polygon(flask, fill=False, ec="#33475b", lw=3))
ax.text(5, -0.3, "liquid in a flask", ha="center", fontsize=14)
ax.annotate("glass walls", (7.6, 3.6), xytext=(6.4, 8.3), fontsize=12, color="tab:red", arrowprops=dict(arrowstyle="->", color="tab:red"))

# balloon with a gas: physical boundary (rubber)
ax = axs[1]
ax.add_patch(Ellipse((5, 6.5), 6.4, 7.4, fc="#ffd27f", ec="#c47f00", lw=3))
ax.plot([5, 5.3, 4.8, 5.2], [2.8, 2.0, 1.2, 0.5], color="0.3", lw=1.5)
for _ in range(14):
    ax.add_patch(Circle((5 + rng.uniform(-2.2, 2.2), 6.5 + rng.uniform(-2.6, 2.6)), 0.18, fc="#c47f00", ec="none"))
ax.text(5, -0.3, "gas in a balloon", ha="center", fontsize=14)
ax.annotate("plastic", (7.9, 8.0), xytext=(8.0, 10.6), fontsize=12, color="tab:red", arrowprops=dict(arrowstyle="->", color="tab:red"))

# cloud: notional boundary
ax = axs[2]
for (x, y, r) in [(3.2, 5.0, 1.8), (5.0, 6.2, 2.3), (7.0, 5.2, 1.8), (4.3, 4.2, 1.6), (6.0, 4.1, 1.7)]:
    ax.add_patch(Circle((x, y), r, fc="#d9e2ec", ec="none"))
th = np.linspace(0, 2 * np.pi, 200)
ax.plot(5.1 + 4.3 * np.cos(th), 5.2 + 3.4 * np.sin(th), "--", color="tab:red", lw=2)
ax.text(5, -0.3, "a cloud", ha="center", fontsize=14)
ax.text(5, 9.6, "boundary set by a condition\n(e.g., water content)", ha="center", fontsize=11, color="tab:red")

# flame: notional boundary
ax = axs[3]
t = np.linspace(0, 2 * np.pi, 300)
for sc, col in [(1.0, "#ff9f1c"), (0.65, "#ffd23f"), (0.35, "#fff3b0")]:
    xs = 5 + sc * 2.2 * np.sin(t) * (1 - 0.15 * np.cos(t))
    ys = 2.6 + sc * 3.4 * (1 - np.cos(t)) ** 0.9
    ax.fill(xs, ys, color=col)
ax.plot(5 + 2.9 * np.sin(t), 2.6 + 4.3 * (1 - np.cos(t)) ** 0.9 - 0.4, "--", color="tab:red", lw=2)
ax.add_patch(Polygon([(4.2, 1.2), (5.8, 1.2), (5.5, 2.6), (4.5, 2.6)], fc="0.5"))
ax.text(5, -0.3, "a flame", ha="center", fontsize=14)
ax.text(5, 11.0, "boundary set by a condition\n(e.g., a temperature)", ha="center", fontsize=11, color="tab:red")
save(fig, f"{out}/ch1_systems.png")
