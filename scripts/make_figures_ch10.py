"""Figure for chapter 10: Gibbs energy vs extent of reaction for N2O4(g) <=> 2 NO2(g).
Usage: python3 scripts/make_figures_ch10.py img"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from figstyle import save, PURPLE

out = sys.argv[1] if len(sys.argv) > 1 else "img"
R, T = 8.314, 298.15
mu_N2O4, mu_NO2 = 99.8e3, 51.3e3          # standard Gibbs energies of formation, J/mol (appendix)
dG0 = 2 * mu_NO2 - mu_N2O4
K = np.exp(-dG0 / (R * T))
xi_eq = np.sqrt(K / (4 + K))               # from K = 4 xi^2 / (1 - xi^2) at P = 1 bar, starting from 1 mol N2O4


def G(xi):
    n1, n2 = 1 - xi, 2 * xi; n = n1 + n2
    mix = sum(ni * np.log(ni / n) for ni in (n1, n2) if ni > 0)
    return n1 * mu_N2O4 + n2 * mu_NO2 + R * T * mix


xi = np.linspace(0, 1, 801)
Gx = (np.array([G(x) for x in xi]) - G(0)) / 1000
Gpure = xi * dG0 / 1000                    # reactants and products kept separate (no mixing)

fig, ax = plt.subplots(figsize=(7.5, 5))
ax.plot(xi, Gpure, "--", color="0.5", lw=2)
ax.plot(xi, Gx, color="tab:blue", lw=2.8)
Geq = (G(xi_eq) - G(0)) / 1000
ax.plot(xi_eq, Geq, "o", color=PURPLE, ms=9, zorder=5)
ax.plot([xi_eq, xi_eq], [-3, Geq], ":", color=PURPLE)
ax.text(xi_eq + 0.02, Geq - 0.25, "equilibrium\n" + r"$\Delta_{\mathrm{rxn}}G=0$", color=PURPLE, fontsize=14, va="top")
ax.text(0.03, -2.35, r"$\Delta_{\mathrm{rxn}}G<0$" + "\nforward\nspontaneous", fontsize=13, color="tab:green", va="center")
ax.text(0.72, -1.5, r"$\Delta_{\mathrm{rxn}}G>0$" + "\nreverse\nspontaneous", fontsize=13, color="tab:red", va="center")
ax.text(0.55, 1.95, "no mixing", color="0.4", fontsize=13, rotation=17)
ax.text(0.01, 0.6, r"pure N$_2$O$_4$", fontsize=12, color="0.3")
ax.text(1.0, dG0 / 1000 + 0.25, r"pure NO$_2$", fontsize=12, color="0.3", ha="right")
ax.set_xlim(0, 1); ax.set_ylim(-3, 3.4)
ax.set_xticks([0, round(xi_eq, 2), 0.5, 1]); ax.set_xticklabels(["0", rf"$\xi_{{\mathrm{{eq}}}}$", "0.5", "1"])
ax.get_xticklabels()[1].set_color(PURPLE)
ax.set_xlabel(r"extent of reaction, $\xi$ [mol]"); ax.set_ylabel(r"$G(\xi)-G(0)$ [kJ]")
save(fig, f"{out}/ch10_G_vs_xi.png")
print(f"dG0 = {dG0/1000:.2f} kJ/mol, K = {K:.3f}, xi_eq = {xi_eq:.3f} mol, G_eq - G(0) = {Geq:.2f} kJ, y_NO2 = {2*xi_eq/(1+xi_eq):.3f}")
