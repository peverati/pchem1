"""Figures for chapter 8. Usage (from the project root): python3 scripts/make_figures_ch8.py img"""
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from machine import draw_machine, draw_machine_ax

out = sys.argv[1] if len(sys.argv) > 1 else "img"
S = ("S", "$S$", "$dS$"); V = ("V", "$V$", "$dV$"); T = ("T", "$T$", "$dT$"); P = ("P", "$P$", "$dP$")
n = ("n", r"$n_i$", r"$dn_i$")
draw_machine(f"{out}/machine_U.png", "$U$", [S, V, n], "")

# Legendre transformations as knob swaps
fig, ax = plt.subplots(figsize=(13, 10))
ax.set_xlim(0, 21); ax.set_ylim(0, 16.5); ax.set_aspect("equal"); ax.axis("off")
s = 0.82
draw_machine_ax(ax, 0.0, 5.5, s, "$U$", [S, V, n], "internal energy")
for y0, disp, knobs, title, lab in [
        (11.0, "$H$", [S, P, n], "enthalpy", r"$H=U+PV$" + "\nswap $V$ for $P$"),
        (5.5, "$A$", [T, V, n], "Helmholtz energy", r"$A=U-TS$" + "\nswap $S$ for $T$"),
        (0.0, "$G$", [T, P, n], "Gibbs energy", r"$G=U-TS+PV$" + "\nswap both")]:
    draw_machine_ax(ax, 12.6, y0, s, disp, knobs, title)
    ax.add_patch(FancyArrowPatch((8.4, 8.0), (13.2, y0 + 2.5), arrowstyle="-|>", mutation_scale=25, lw=2.5, color="tab:purple",
                                 connectionstyle="arc3,rad=0.0"))
    # labels beside the arrows, never on them: above the upper and middle arrows, below the lower one
    x, y, ha, va = {11.0: (10.3, 11.2, "right", "bottom"), 5.5: (10.8, 8.35, "center", "bottom"), 0.0: (10.3, 4.8, "right", "top")}[y0]
    ax.text(x, y, lab, ha=ha, va=va, fontsize=14, color="tab:purple")
fig.savefig(f"{out}/ch8_legendre_machines.png", dpi=200, bbox_inches="tight")
print("saved", f"{out}/ch8_legendre_machines.png")
