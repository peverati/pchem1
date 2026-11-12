"""Figures for chapter 2 (work in isothermal expansions). Usage: python3 scripts/make_figures_ch2.py img"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from figstyle import save, PURPLE

out = sys.argv[1] if len(sys.argv) > 1 else "img"
nRT = 0.08314 * 298          # L bar, 1 mol of ideal gas at 298 K
P = lambda V: nRT / V
V = np.linspace(0.12, 1.25, 400)
Vi, V1, Vf = 0.2, 0.5, 1.0


def base(Vi=Vi, mid=False):
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ax.plot(V, P(V), color="tab:blue", lw=2.5, label="isotherm, 298 K")
    pts = [(Vi, "i"), (Vf, "f")] + ([(V1, "1")] if mid else [])
    for v, lab in pts:
        ax.plot(v, P(v), "o", color=PURPLE, ms=9, zorder=5)
        ax.annotate(lab, (v, P(v)), xytext=(8, 6), textcoords="offset points", fontsize=17, color=PURPLE)
        ax.plot([v, v], [0, P(v)], ":", color="gray"); ax.plot([0, v], [P(v), P(v)], ":", color="gray")
    ax.set_xlim(0, 1.25); ax.set_ylim(0, 140)
    ax.set_xlabel("Volume [L]"); ax.set_ylabel("Pressure [bar]")
    return ax, fig


def hatch(ax, v0, v1, p, color, label):
    ax.fill_between([v0, v1], 0, p, facecolor="none", edgecolor=color, hatch="///", lw=1.5)
    ax.text((v0 + v1) / 2, p / 2, label, ha="center", va="center", fontsize=15,
            bbox=dict(fc="white", ec="none", alpha=0.9))


ax, fig = base(Vi=0.25); save(fig, f"{out}/ch2_pv_isotherm.png")

ax, fig = base(); hatch(ax, Vi, Vf, P(Vf), "tab:red", r"$P_f\,(V_f-V_i)$")
save(fig, f"{out}/ch2_pv_1step.png")

ax, fig = base(mid=True); hatch(ax, Vi, V1, P(V1), "tab:blue", r"$P_1\,(V_1-V_i)$")
save(fig, f"{out}/ch2_pv_2stepA.png")

ax, fig = base(mid=True); hatch(ax, V1, Vf, P(Vf), "tab:green", r"$P_f\,(V_f-V_1)$")
save(fig, f"{out}/ch2_pv_2stepB.png")

ax, fig = base(mid=True)
ax.fill_between([Vi, V1], 0, P(V1), facecolor="none", edgecolor="tab:blue", hatch="///", lw=1.5)
ax.fill_between([V1, Vf], 0, P(Vf), facecolor="none", edgecolor="tab:green", hatch="///", lw=1.5)
ax.text(0.5, 12, r"$|W_{\mathrm{2\text{-}step}}|$", ha="center", fontsize=16, bbox=dict(fc="white", ec="none"))
save(fig, f"{out}/ch2_pv_2step.png")

ax, fig = base()
Vs = np.linspace(Vi, Vf, 200)
ax.fill_between(Vs, 0, P(Vs), color="0.6", alpha=0.6)
for n, col in [(6, "tab:orange"), (30, "tab:green")]:
    edges = np.linspace(Vi, Vf, n + 1)
    for a, b in zip(edges[:-1], edges[1:]):
        ax.plot([a, a, b], [P(a), P(b), P(b)], color=col, lw=1.5 if n < 20 else 1.0)
ax.text(0.5, 12, r"$|W_{\max}|$", ha="center", fontsize=17, bbox=dict(fc="white", ec="none"))
ax.text(0.62, 80, "6 steps", color="tab:orange", fontsize=14); ax.text(0.62, 68, "30 steps", color="tab:green", fontsize=14); ax.text(0.62, 56, r"$\infty$ steps", color="0.4", fontsize=14)
save(fig, f"{out}/ch2_pv_max.png")
