"""Figures for chapters 6, 7, and 9: entropy of water vs T and the unattainability of 0 K (ch. 6),
Hess cycle for methane combustion (ch. 7), and Gibbs energy of reaction vs T for the four sign combinations of Delta H and Delta S.
Usage: python3 scripts/make_figures_ch6_7_9.py img"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from figstyle import save, PURPLE

out = sys.argv[1] if len(sys.argv) > 1 else "img"

# ---------- ch. 4: enthalpy-level diagram of the Hess cycle (data of eq-someDfH) ----------
H_el, H_r, H_p = 0.0, -75.0, -394.0 + 2 * (-286.0)
fig, ax = plt.subplots(figsize=(7.5, 5.2))
def arrow(x0, y0, x1, y1, col):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2, mutation_scale=18))
ax.plot([0.55, 1.95], [H_el] * 2, color="0.3", lw=4, solid_capstyle="butt")
ax.text(1.97, H_el + 22, r"C$_{(s)}$ + 2 H$_{2(g)}$ + 2 O$_{2(g)}$ (elements)", ha="right", fontsize=13, color="0.3")
ax.plot([-0.1, 0.8], [H_r] * 2, color="tab:blue", lw=4, solid_capstyle="butt")
ax.text(0.35, H_r - 50, r"CH$_{4(g)}$ + 2 O$_{2(g)}$", ha="center", fontsize=13, color="tab:blue")
ax.plot([1.2, 2.0], [H_p] * 2, color="tab:red", lw=4, solid_capstyle="butt")
ax.text(1.6, H_p - 55, r"CO$_{2(g)}$ + 2 H$_2$O$_{(l)}$", ha="center", fontsize=13, color="tab:red")
arrow(0.65, H_el - 3, 0.65, H_r + 3, "tab:blue")
arrow(1.75, H_el - 3, 1.75, H_p + 3, "tab:red")
ax.text(1.8, (H_el + H_p) / 2, r"$\Delta_{\mathrm{f}}H^{\ominus}_{\mathrm{CO_2}}$" + "\n" + r"$+\,2\,\Delta_{\mathrm{f}}H^{\ominus}_{\mathrm{H_2O}}$" + "\n" + r"$= -966$", fontsize=12, color="tab:red", va="center")
arrow(0.4, H_r - 70, 1.3, H_p + 3, PURPLE)
ax.text(0.62, (H_r + H_p) / 2 - 20, r"$\Delta_{\mathrm{rxn}}H^{\ominus}$" + "\n" + r"$= -966-(-75)$" + "\n" + r"$= -891\;\mathrm{kJ/mol}$", fontsize=13, color=PURPLE, ha="right", va="center")
ax.text(-0.17, H_r, r"$\Delta_{\mathrm{f}}H^{\ominus}_{\mathrm{CH_4}} = -75$", fontsize=12, color="tab:blue", ha="right", va="center")
ax.set_xlim(-1.05, 2.5); ax.set_ylim(-1060, 70)
ax.set_xticks([]); ax.spines["bottom"].set_visible(False)
ax.set_ylabel(r"$H^{\ominus}$ relative to the elements [kJ/mol]")
save(fig, f"{out}/ch7_hess_methane.png")

# ---------- ch. 7: absolute entropy of water at 1 bar vs T (approximate heat capacities) ----------
Tm, Tb = 273.15, 373.15
dHfus, dHvap = 6010.0, 40650.0
Cp_ice = lambda T: 37.8 * (T / Tm) ** 0.86            # simple fit to the heat capacity of ice (about 38 J/(mol K) at 0 C)
Cp_liq, Cp_gas = 75.3, 33.6
T1 = np.linspace(1e-3, Tm, 300); S1 = 37.8 / 0.86 * (T1 / Tm) ** 0.86      # integral of Cp/T from 0
S_m_s = S1[-1]; S_m_l = S_m_s + dHfus / Tm
T2 = np.linspace(Tm, Tb, 200); S2 = S_m_l + Cp_liq * np.log(T2 / Tm)
S_b_l = S2[-1]; S_b_g = S_b_l + dHvap / Tb
T3 = np.linspace(Tb, 450, 100); S3 = S_b_g + Cp_gas * np.log(T3 / Tb)
fig, ax = plt.subplots(figsize=(7.5, 5))
ax.plot(T1, S1, color="tab:blue", lw=2.8); ax.plot(T2, S2, color="tab:green", lw=2.8); ax.plot(T3, S3, color="tab:red", lw=2.8)
ax.plot([Tm, Tm], [S_m_s, S_m_l], ":", color=PURPLE, lw=2); ax.plot([Tb, Tb], [S_b_l, S_b_g], ":", color=PURPLE, lw=2)
ax.text(Tm - 6, (S_m_s + S_m_l) / 2, r"$\frac{\Delta_{\mathrm{fus}}H}{T_{\mathrm{m}}}$", color=PURPLE, fontsize=17, ha="right", va="center")
ax.text(Tb - 6, (S_b_l + S_b_g) / 2, r"$\frac{\Delta_{\mathrm{vap}}H}{T_{\mathrm{b}}}$", color=PURPLE, fontsize=17, ha="right", va="center")
ax.text(150, 18, "ice", color="tab:blue", fontsize=15); ax.text(300, S_m_l - 14, "liquid", color="tab:green", fontsize=15)
ax.text(400, S_b_g - 18, "vapor", color="tab:red", fontsize=15)
ax.plot(0, 0, "o", color=PURPLE, ms=8, clip_on=False, zorder=5)
ax.annotate(r"third law: $S=0$ at $0\;\mathrm{K}$", (0, 0), xytext=(15, 100), textcoords="data", color=PURPLE, fontsize=13,
            arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=1.2, mutation_scale=15, shrinkB=6))
ax.set_xlim(0, 450); ax.set_ylim(0, 220)
ax.set_xticks([0, 100, 200, Tm, Tb]); ax.set_xticklabels(["0", "100", "200", r"$T_{\mathrm{m}}$", r"$T_{\mathrm{b}}$"])
ax.set_xlabel("Temperature [K]"); ax.set_ylabel(r"$S$ [J/(mol K)]")
save(fig, f"{out}/ch6_S_vs_T_water.png")
print(f"S(ice, Tm) = {S_m_s:.1f}, S(liq, Tm) = {S_m_l:.1f}, S(liq, 298) = {S_m_l + Cp_liq*np.log(298.15/Tm):.1f}, "
      f"S(liq, Tb) = {S_b_l:.1f}, S(gas, Tb) = {S_b_g:.1f}")

# ---------- ch. 7: unattainability of absolute zero (cooling by alternating isothermal and adiabatic steps) ----------
Tg = np.linspace(0, 1, 300)
S1 = lambda T: 1.0 * T ** 0.8          # entropy with the control parameter at its first value (e.g., zero magnetic field)
S2 = lambda T: 0.55 * T ** 0.8         # second value (e.g., high field): lower entropy at the same T; both reach S = 0 at T = 0
fig, ax = plt.subplots(figsize=(7.5, 5))
ax.plot(Tg, S1(Tg), color="tab:blue", lw=2.6); ax.plot(Tg, S2(Tg), color="tab:red", lw=2.6)
ax.text(0.93, S1(0.93) + 0.04, "parameter $X_1$", color="tab:blue", fontsize=13, ha="right")
ax.text(0.97, S2(0.7) - 0.05, "parameter $X_2$", color="tab:red", fontsize=13, ha="right", va="top")
T = 0.9
for k in range(7):
    s_hi, s_lo = S1(T), S2(T)
    ax.plot([T, T], [s_hi, s_lo], color=PURPLE, lw=1.8)                       # isothermal step: X1 -> X2
    Tn = (s_lo / 1.0) ** (1 / 0.8)                                             # adiabatic step: X2 -> X1 at constant S
    ax.plot([T, Tn], [s_lo, s_lo], color=PURPLE, lw=1.8, ls="--")
    T = Tn
ax.text(0.89, (S1(0.9) + S2(0.9)) / 2, "isothermal", color=PURPLE, fontsize=12, va="center", ha="right")
ax.text(0.62, S2(0.9) + 0.025, "adiabatic", color=PURPLE, fontsize=12)
ax.plot(0, 0, "o", color="k", ms=7, clip_on=False, zorder=5)
ax.annotate("both curves reach $S=0$\nat $T=0$ (third law)", (0, 0), xytext=(0.12, 0.62), fontsize=12,
            arrowprops=dict(arrowstyle="-", color="0.3", lw=1))
ax.set_xlim(0, 1); ax.set_ylim(0, 1.0); ax.set_xticks([0]); ax.set_yticks([])
ax.set_xlabel("$T$"); ax.set_ylabel("$S$")
save(fig, f"{out}/ch6_unattainability.png")

# ---------- ch. 9: Delta G = Delta H - T Delta S for the four sign combinations ----------
T = np.linspace(0, 1000, 200)
cases = [(50, -0.1, "tab:orange", r"$\Delta H>0,\ \Delta S<0$: never spontaneous"),
         (-50, -0.1, "tab:blue", r"$\Delta H<0,\ \Delta S<0$: spontaneous at low $T$"),
         (50, 0.1, "tab:red", r"$\Delta H>0,\ \Delta S>0$: spontaneous at high $T$"),
         (-50, 0.1, "tab:green", r"$\Delta H<0,\ \Delta S>0$: always spontaneous")]
fig, ax = plt.subplots(figsize=(7, 5.2))
ax.axhspan(-170, 0, color="tab:green", alpha=0.07); ax.axhline(0, color="k", lw=1)
ax.text(25, -160, r"$\Delta G<0$: spontaneous", fontsize=13, color="tab:green")
ax.text(25, 160, r"$\Delta G>0$: not spontaneous", fontsize=13, color="0.35", va="top")
for dH, dS, col, lab in cases:
    ax.plot(T, dH - T * dS, color=col, lw=2.6)
    ax.text(1015, dH - 1000 * dS, lab, color=col, fontsize=12, va="center", clip_on=False)
ax.plot(500, 0, "o", color=PURPLE, ms=9, zorder=5)
ax.annotate(r"$T=\frac{\Delta H}{\Delta S}$", (500, 0), xytext=(0, 24), textcoords="offset points", color=PURPLE, fontsize=16, ha="center")
ax.set_xlim(0, 1000); ax.set_ylim(-170, 170)
ax.set_xticks([0]); ax.set_yticks([0]); ax.set_xlabel("$T$"); ax.set_ylabel(r"$\Delta G = \Delta H - T\Delta S$")
save(fig, f"{out}/ch9_dG_vs_T.png")
