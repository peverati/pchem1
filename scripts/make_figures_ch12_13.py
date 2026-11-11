"""Computed phase diagrams for chapters 12 and 13. Usage: python3 scripts/make_figures_ch12_13.py img"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from scipy.optimize import brentq
from figstyle import save, PURPLE

out = sys.argv[1] if len(sys.argv) > 1 else "img"
Rj = 8.314

# =================== chapter 12 ===================
# chemical potential vs temperature (water-like entropies, J/(mol K))
T = np.linspace(180, 470, 400)
Tm, Tb = 273.0, 373.0
S_s, S_l, S_g = 30.0, 75.0, 180.0           # schematic entropies: S_gas >> S_liquid > S_solid
curv = 0.03                                  # small downward curvature (S increases with T)
mu_l = lambda T: (-S_l * (T - Tm) - curv * (T - Tm) ** 2) / 1000
mu_s = lambda T: (-S_s * (T - Tm) - curv * (T - Tm) ** 2) / 1000
mu_g0 = lambda T: mu_l(Tb) + (-S_g * (T - Tb) - curv * (T - Tb) ** 2) / 1000


def mu_plot(ax, shift_g=0.0, shift_l=0.0, color_lines="k", highlight=True, label=True, alpha=1.0):
    g = lambda T: mu_g0(T) + shift_g
    l = lambda T: mu_l(T) + shift_l
    for f, name in [(mu_s, "solid"), (l, "liquid"), (g, "gas")]:
        ax.plot(T, f(T), color=color_lines, lw=2, alpha=alpha)
        if label:
            ax.text(T[-1] + 4, f(T[-1]), name, fontsize=14, color=color_lines, alpha=alpha, va="center")
    if highlight:
        low = np.minimum(np.minimum(mu_s(T), l(T)), g(T))
        ax.plot(T, low, color="tab:red", lw=6, alpha=0.35, zorder=0)
    tm = brentq(lambda t: mu_s(t) - l(t), 200, 360)
    tb = brentq(lambda t: l(t) - g(t), 280, 465)
    return tm, tb


fig, ax = plt.subplots(figsize=(7.5, 5))
tm, tb = mu_plot(ax)
for t, lab, col in [(tm, r"$T_{\mathrm{m}}$", "tab:green"), (tb, r"$T_{\mathrm{b}}$", "tab:blue")]:
    ax.axvline(t, ls=":", color=col); ax.text(t + 3, -38, lab, color=col, fontsize=16)
    ax.plot(t, mu_s(t) if col == "tab:green" else mu_l(t), "o", color=PURPLE, ms=8, zorder=5)
ax.plot([], [], color="tab:red", lw=6, alpha=0.35, label="most stable phase"); ax.legend(frameon=False, loc="upper right")
ax.set_xlabel("$T$"); ax.set_ylabel(r"$\mu$"); ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(-40, 12); ax.set_xlim(175, 510)
save(fig, f"{out}/ch12_mu_vs_T.png")

fig, ax = plt.subplots(figsize=(7.5, 5))
tm1, tb1 = mu_plot(ax, highlight=False, color_lines="0.6", label=False)
shift = Rj * 300 * np.log(0.1) / 1000          # pressure lowered tenfold: gas shifts, condensed phases almost do not
tm2, tb2 = mu_plot(ax, shift_g=shift, highlight=False, label=False)
for f_, name in [(mu_s, "solid"), (mu_l, "liquid"), (lambda T: mu_g0(T) + shift, r"gas, $P_2<P_1$")]:
    ax.text(T[-1] + 4, f_(T[-1]), name, fontsize=14, va="center")
ax.text(T[-1] + 4, mu_g0(T[-1]), r"gas, $P_1$", color="0.5", fontsize=13, va="center")
ax.annotate("", xy=(425, mu_g0(425) + shift), xytext=(425, mu_g0(425)), arrowprops=dict(arrowstyle="->", color=PURPLE, lw=2))
for t1, t2, col, lab in [(tm1, tm2, "tab:green", r"$T_{\mathrm{m}}$"), (tb1, tb2, "tab:blue", r"$T_{\mathrm{b}}$")]:
    ax.axvline(t1, ls=":", color="0.6"); ax.axvline(t2, ls=":", color=col)
    ax.text(t2 + 2, -38 if col == 'tab:green' else -34, lab + r"$(P_2)$", color=col, fontsize=13)
ax.text(tb1 + 3, -30, r"$T_{\mathrm{b}}(P_1)$", color="0.5", fontsize=13)
# junction points: purple at P2, faded purple at P1
ax.plot([tm2, tb2], [mu_s(tm2), mu_l(tb2)], "o", color=PURPLE, ms=8, zorder=5)
ax.plot(tb1, mu_l(tb1), "o", color=PURPLE, ms=8, alpha=0.45, zorder=5)
ax.set_xlabel("$T$"); ax.set_ylabel(r"$\mu$"); ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(-40, 12); ax.set_xlim(175, 520)
save(fig, f"{out}/ch12_mu_pressure.png")

# PT diagram of CO2 (Clausius-Clapeyron), with a water-like anomalous melting line
Ttp, Ptp, Tc, Pc = 216.6, 5.18, 304.1, 73.8
dH_vap = Rj * np.log(Pc / Ptp) / (1 / Ttp - 1 / Tc)
dH_sub = 26100.0
fig, ax = plt.subplots(figsize=(7.5, 5.2))
Ts = np.linspace(170, Ttp, 100); ax.plot(Ts, Ptp * np.exp(-dH_sub / Rj * (1 / Ts - 1 / Ttp)), color="tab:red", lw=2.5)
Tv = np.linspace(Ttp, Tc, 100); ax.plot(Tv, Ptp * np.exp(-dH_vap / Rj * (1 / Tv - 1 / Ttp)), color="tab:blue", lw=2.5)
Pf = np.geomspace(Ptp, 2000, 50); ax.plot(Ttp + (Pf - Ptp) / 200, Pf, color="tab:green", lw=2.5)
ax.plot(Ttp - (Pf - Ptp) / 200, Pf, "--", color="tab:green", lw=2)
ax.text(Ttp - 28, 900, "anomalous\n(water-like)", color="tab:green", fontsize=11, ha="center")
ax.plot(Ttp, Ptp, "o", color="tab:orange", ms=9, zorder=5); ax.plot(Tc, Pc, "o", color="tab:red", ms=9, zorder=5)
ax.annotate("triple point", (Ttp, Ptp), xytext=(7, -15), textcoords="offset points", color="tab:orange", fontsize=13)
ax.annotate("critical point", (Tc, Pc), xytext=(-40, 12), textcoords="offset points", color="tab:red", fontsize=13)
ax.axhline(Pc, ls=":", color="tab:red", lw=1); ax.axvline(Tc, ls=":", color="tab:red", lw=1)
ax.axhline(1, ls="--", color="0.5", lw=1); ax.text(172, 1.12, "1 bar", color="0.4", fontsize=12)
for x, y, t in [(195, 30, "solid"), (255, 45, "liquid"), (262, 600, "compressible\nliquid"), (326, 500, "supercritical\nfluid"),
                (262, 9, "vapor"), (326, 15, "gas")]:
    ax.text(x, y, t, fontsize=14, ha="center", va="center")
ax.set_yscale("log"); ax.set_xlim(170, 350); ax.set_ylim(0.3, 2000)
ax.set_yticks([1, 10, Pc, 1000]); ax.set_yticklabels(["1", "10", r"$P_c$", "1000"])
ax.set_xticks([175, 200, 225, 250, 275, Tc, 325]); ax.set_xticklabels(["175", "200", "225", "250", "275", r"$T_c$", "325"])
ax.set_xlabel("Temperature [K]"); ax.set_ylabel("Pressure [bar] (log scale)")
save(fig, f"{out}/ch12_PT_CO2.png")

# =================== chapter 13 ===================
def antoine(T_C, A, B, C):        # bar
    return 10 ** (A - B / (C + T_C)) / 750.06
benz = lambda t: antoine(t, 6.90565, 1211.033, 220.790)   # component B (more volatile)
tol = lambda t: antoine(t, 6.95464, 1344.800, 219.482)    # component A
x = np.linspace(0, 1, 201)


def frame(ax, ylabel, left=None, right=None):
    """Composition diagram with an axis for pure A (left) and one for pure B (right).
    left/right: (value, label) of the pure-component point, written outside the axes."""
    ax.set_xlim(0, 1); ax.set_xlabel(r"$x_{\mathrm{B}}$ (mole fraction of B)"); ax.set_ylabel(ylabel, labelpad=58 if left else 4)
    ax.spines["right"].set_visible(True); ax.tick_params(right=True, labelright=True)
    ax.text(0, -0.13, "A", transform=ax.transAxes, ha="center"); ax.text(1, -0.13, "B", transform=ax.transAxes, ha="center")
    if left:
        ax.annotate(left[1], xy=(0, left[0]), xycoords=("axes fraction", "data"), xytext=(-52, 0), textcoords="offset points",
                    ha="right", va="center", fontsize=15, color="tab:orange", annotation_clip=False,
                    arrowprops=dict(arrowstyle="-", color="tab:orange", lw=1))
    if right:
        ax.annotate(right[1], xy=(1, right[0]), xycoords=("axes fraction", "data"), xytext=(52, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=15, color="tab:orange", annotation_clip=False,
                    arrowprops=dict(arrowstyle="-", color="tab:orange", lw=1))


# one volatile component
fig, ax = plt.subplots(figsize=(7, 5))
PA = tol(25)
ax.plot(x, (1 - x) * PA, color="k", lw=2.5)
ax.plot(0, PA, "o", color="tab:orange", ms=9, clip_on=False, zorder=5)
ax.text(0.6, 0.032, "liquid", fontsize=15); ax.text(0.15, 0.008, "vapor", fontsize=15)
ax.set_ylim(0, 0.045); frame(ax, "Pressure [bar]", left=(PA, r"$P_{\mathrm{A}}^*$"))
ax.set_title("toluene (A) + nonvolatile solute (B), 25 °C", fontsize=14)
save(fig, f"{out}/ch13_Px_one_volatile.png")

# two volatile components: partial and total pressures
PA, PB = tol(25), benz(25)
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(x, (1 - x) * PA, ":", color="k", lw=2); ax.plot(x, x * PB, ":", color="k", lw=2)
ax.plot(x, (1 - x) * PA + x * PB, color="tab:red", lw=2.5)
ax.text(0.03, 0.006, r"$P_{\mathrm{A}}$", fontsize=14); ax.text(0.86, 0.085, r"$P_{\mathrm{B}}$", fontsize=14)
ax.text(0.4, 0.085, r"$P_{\mathrm{TOT}}$", color="tab:red", fontsize=15)
ax.text(0.2, 0.11, "liquid", fontsize=15); ax.text(0.7, 0.03, "vapor", fontsize=15)
ax.plot([0, 1], [PA, PB], "o", color="tab:orange", ms=9, clip_on=False, zorder=5)
ax.set_ylim(0, 0.14); frame(ax, "Pressure [bar]", (PA, r"$P_{\mathrm{A}}^*$"), (PB, r"$P_{\mathrm{B}}^*$")); ax.set_title("toluene (A) + benzene (B), 25 °C", fontsize=14)
save(fig, f"{out}/ch13_Px_ideal.png")

# liquidus and dew point lines
Pliq = (1 - x) * PA + x * PB
ydew = x * PB / Pliq
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(x, Pliq, color="tab:red", lw=2.5); ax.plot(ydew, Pliq, color="tab:blue", lw=2.5)
ax.fill_betweenx(Pliq, ydew, x, color="0.85")
xi = 0.4; Pi = (1 - xi) * PA + xi * PB; yi = xi * PB / Pi
ax.annotate("", xy=(xi, Pi), xytext=(xi, 0.125), arrowprops=dict(arrowstyle="->", color=PURPLE, lw=2))
ax.plot([xi, yi], [Pi, Pi], "--", color=PURPLE, lw=1.8); ax.plot([xi, yi], [Pi, Pi], "o", color=PURPLE, ms=8, zorder=5); ax.plot(xi, 0.125, "o", color=PURPLE, ms=8)
ax.text(xi + 0.01, 0.127, "$i$", color=PURPLE, fontsize=15)
ax.annotate(r"$x_{\mathrm{B}}^i$", (xi, 0), xytext=(xi - 0.03, 0.004), fontsize=14, color=PURPLE)
ax.annotate(r"$y_{\mathrm{B}}^f$", (yi, 0), xytext=(yi - 0.03, 0.004), fontsize=14, color=PURPLE)
ax.plot([xi, xi], [0, Pi], ":", color=PURPLE); ax.plot([yi, yi], [0, Pi], ":", color=PURPLE)
ax.text(0.08, 0.11, "liquid", fontsize=15); ax.text(0.75, 0.03, "vapor", fontsize=15)
ax.text(0.55, 0.1, "liquidus\n(bubble point) line", color="tab:red", fontsize=12)
ax.text(0.68, 0.06, "dew point line", color="tab:blue", fontsize=12)
ax.text(0.53, 0.068, "liquid\n+ vapor", fontsize=12, ha="center")
ax.plot([0, 1], [PA, PB], "o", color="tab:orange", ms=9, clip_on=False, zorder=5)
ax.set_ylim(0, 0.14); frame(ax, "Pressure [bar]", (PA, r"$P_{\mathrm{A}}^*$"), (PB, r"$P_{\mathrm{B}}^*$")); ax.set_title("toluene (A) + benzene (B), 25 °C", fontsize=14)
save(fig, f"{out}/ch13_Px_liquidus_dew.png")

# Tx diagram at 1 atm
P0 = 1.01325
Tbub = np.array([brentq(lambda t: (1 - xx) * tol(t) + xx * benz(t) - P0, 60, 130) for xx in x])
ybub = x * benz(Tbub) / P0


def tx_base(ax):
    ax.plot(x, Tbub, color="tab:red", lw=2.5); ax.plot(ybub, Tbub, color="tab:blue", lw=2.5)
    ax.fill_betweenx(Tbub, x, ybub, color="0.85")
    ax.plot([0, 1], [Tbub[0], Tbub[-1]], "o", color="tab:orange", ms=9, clip_on=False, zorder=5)
    ax.set_ylim(75, 115); frame(ax, "Temperature [°C]", (Tbub[0], r"$T_{\mathrm{b}}^{\mathrm{A}}$"), (Tbub[-1], r"$T_{\mathrm{b}}^{\mathrm{B}}$"))


fig, ax = plt.subplots(figsize=(7, 5))
tx_base(ax)
xi = 0.3; Ti = np.interp(xi, x, Tbub); yi = np.interp(xi, x, ybub)
ax.annotate("", xy=(xi, Ti), xytext=(xi, 78), arrowprops=dict(arrowstyle="->", color=PURPLE, lw=2))
ax.plot(xi, 78, "o", color=PURPLE, ms=8); ax.text(xi + 0.015, 78, "$i$", color=PURPLE, fontsize=15)
ax.plot([xi, yi], [Ti, Ti], "--", color=PURPLE); ax.plot([xi, yi], [Ti, Ti], "o", color=PURPLE, ms=8, zorder=5)
ax.annotate(r"$x_{\mathrm{B}}^i$", (xi, 75), xytext=(xi + 0.01, 75.5), fontsize=14, color=PURPLE)
ax.annotate(r"$y_{\mathrm{B}}^f$", (yi, Ti), xytext=(yi + 0.01, Ti + 1), fontsize=14, color=PURPLE)
ax.text(0.75, 108, "vapor", fontsize=15); ax.text(0.08, 82, "liquid", fontsize=15)
ax.text(0.12, 112, "dew point line", color="tab:blue", fontsize=12); ax.text(0.62, 86, "liquidus line", color="tab:red", fontsize=12)
ax.set_title("toluene (A) + benzene (B), 1 atm", fontsize=14)
save(fig, f"{out}/ch13_Tx_ideal.png")

# fractional distillation: staircase + column
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [2.2, 1]}); fig.subplots_adjust(wspace=0.3)
tx_base(ax)
xs = 0.15; steps = 0
while xs < 0.95 and steps < 6:
    Tn = np.interp(xs, x, Tbub); yn = np.interp(xs, x, ybub)
    ax.plot([xs, yn], [Tn, Tn], color=PURPLE, lw=2); Tnext = np.interp(yn, x, Tbub)
    ax.plot([yn, yn], [Tn, Tnext], color=PURPLE, lw=2)
    steps += 1; ax.text((xs + yn) / 2, Tn + 0.6, str(steps), color=PURPLE, fontsize=12, ha="center")
    xs = yn
ax.set_title("theoretical plates", fontsize=14)
ax2.axis("off"); ax2.set_xlim(0, 4); ax2.set_ylim(0, 10)
ax2.add_patch(Rectangle((1, 1), 2, 8, fc="#e8eef5", ec="0.3", lw=2))
for yy in np.linspace(2, 8, 6):
    ax2.plot([1.1, 2.6] if int(yy) % 2 == 0 else [1.4, 2.9], [yy, yy], color="0.3", lw=2)
ax2.add_patch(FancyArrowPatch((2, 9), (2, 9.9), arrowstyle="-|>", mutation_scale=18, color="tab:blue"))
ax2.text(2, 9.95, "vapor rich in B\n(to condenser)", ha="center", va="bottom", fontsize=11, color="tab:blue")
ax2.add_patch(FancyArrowPatch((2, 1), (2, 0.1), arrowstyle="-|>", mutation_scale=18, color="tab:red"))
ax2.text(2, 0.0, "liquid rich in A", ha="center", va="top", fontsize=11, color="tab:red")
ax2.add_patch(FancyArrowPatch((0.1, 5), (1, 5), arrowstyle="-|>", mutation_scale=18, color="k"))
ax2.text(0.05, 5.3, "feed", fontsize=11)
ax2.text(3.15, 5, "trays\n(plates)", fontsize=11, va="center")
ax2.text(3.15, 1.4, "heat", fontsize=11, color="tab:red"); ax2.text(3.15, 8.4, "cooler", fontsize=11, color="tab:blue")
save(fig, f"{out}/ch13_distillation.png")


# non-ideal solutions (one-parameter Margules model, ln gamma_A = W x_B^2)
def margules_fig(ax, PA, PB, W, title):
    gA = np.exp(W * x ** 2); gB = np.exp(W * (1 - x) ** 2)
    pa = (1 - x) * gA * PA; pb = x * gB * PB
    ax.plot(x, (1 - x) * PA + x * PB, color="0.6", lw=1, ls="--")
    ax.plot(x, pa, ":", color="k", lw=2); ax.plot(x, pb, ":", color="k", lw=2)
    ax.plot(x, pa + pb, color="tab:red", lw=2.5)
    ax.plot([0, 1], [PA, PB], "o", color="tab:orange", ms=8, clip_on=False, zorder=5)
    ax.set_ylim(0, 1.6); frame(ax, "Pressure [bar]", (PA, r"$P_{\mathrm{A}}^*$"), (PB, r"$P_{\mathrm{B}}^*$")); ax.set_title(title, fontsize=14)


fig, ax = plt.subplots(figsize=(7, 5))
W, PA = 1.0, 1.0
pa = (1 - x) * np.exp(W * x ** 2) * PA
ax.plot(x, pa, color="k", lw=2.5)
ax.plot(x, (1 - x) * PA, ":", color="tab:blue", lw=2); ax.text(0.45, 0.42, "Raoult's law", color="tab:blue", fontsize=14)
xh = np.linspace(0.6, 1, 50); ax.plot(xh, (1 - xh) * PA * np.exp(W), ":", color="tab:green", lw=2.5)
ax.text(0.62, 0.9, "Henry's law", color="tab:green", fontsize=14)
ax.plot(0, PA, "o", color="tab:orange", ms=9, clip_on=False, zorder=5)
ax.text(0.1, 1.15, "liquid", fontsize=15); ax.text(0.15, 0.2, "vapor", fontsize=15)
ax.set_ylim(0, 1.3); frame(ax, "Pressure [bar]", left=(PA, r"$P_{\mathrm{A}}^*$")); ax.set_title("only A is volatile (model mixture)", fontsize=14)
save(fig, f"{out}/ch13_Px_henry.png")

fig, axs = plt.subplots(1, 2, figsize=(14, 4.8)); fig.subplots_adjust(wspace=0.9)
margules_fig(axs[0], 0.6, 1.0, 1.4, "positive deviation")
margules_fig(axs[1], 0.6, 1.0, -1.4, "negative deviation")
save(fig, f"{out}/ch13_Px_nonideal.png")


# Tx with azeotropes (model mixture: Clausius-Clapeyron vapor pressures + Margules)
def Psat(T, Tb, dH=35000.0):
    return P0 * np.exp(-dH / Rj * (1 / T - 1 / Tb))


def tx_nonideal(ax, W, title):
    TbA, TbB = 360.0, 352.0
    Tl, yv = [], []
    for xx in x:
        gA, gB = np.exp(W * xx ** 2), np.exp(W * (1 - xx) ** 2)
        f = lambda t: (1 - xx) * gA * Psat(t, TbA) + xx * gB * Psat(t, TbB) - P0
        t = brentq(f, 250, 450); Tl.append(t); yv.append(xx * gB * Psat(t, TbB) / P0)
    Tl = np.array(Tl) - 273.15; yv = np.array(yv)
    ax.plot(x, Tl, color="tab:red", lw=2.5); ax.plot(yv, Tl, color="tab:blue", lw=2.5)
    k = np.argmin(Tl) if W > 0 else np.argmax(Tl)
    ax.plot(x[k], Tl[k], "o", color=PURPLE, ms=9, zorder=5)
    ax.annotate("azeotrope", (x[k], Tl[k]), xytext=(0, -24 if W > 0 else 14), textcoords="offset points", ha="center", color=PURPLE, fontsize=13)
    ax.plot([0, 1], [Tl[0], Tl[-1]], "o", color="tab:orange", ms=8, clip_on=False, zorder=5)
    frame(ax, "Temperature [°C]", (Tl[0], r"$T_{\mathrm{b}}^{\mathrm{A}}$"), (Tl[-1], r"$T_{\mathrm{b}}^{\mathrm{B}}$")); ax.set_title(title, fontsize=14)
    ax.set_ylim(Tl.min() - 6, Tl.max() + 8 if W > 0 else Tl.max() + 6)


fig, axs = plt.subplots(1, 2, figsize=(14, 4.8)); fig.subplots_adjust(wspace=0.9)
tx_nonideal(axs[0], 1.2, "minimum-boiling (positive) azeotrope")
tx_nonideal(axs[1], -1.2, "maximum-boiling (negative) azeotrope")
save(fig, f"{out}/ch13_Tx_azeotropes.png")

# activity coefficients from the vapor pressure of A
fig, axs = plt.subplots(1, 2, figsize=(14, 4.8)); fig.subplots_adjust(wspace=0.9)
for ax, W, title in [(axs[0], 1.0, r"$\gamma_{\mathrm{A}}>1$"), (axs[1], -1.0, r"$0<\gamma_{\mathrm{A}}<1$")]:
    PA = 1.0; pa = (1 - x) * np.exp(W * x ** 2) * PA
    ax.plot(x, pa, color="k", lw=2.5); ax.plot(x, (1 - x) * PA, ":", color="tab:blue", lw=2)
    xb = 0.6; pm = (1 - xb) * np.exp(W * xb ** 2) * PA; pr = (1 - xb) * PA
    ax.plot([xb, xb], [0, max(pm, pr)], ":", color="0.4")
    ax.plot(xb, pm, "o", color="tab:red", ms=8); ax.plot(xb, pr, "o", color="tab:blue", ms=8)
    ax.annotate(r"$P_{\mathrm{A}}$", (xb, pm), xytext=(8, 4), textcoords="offset points", color="tab:red")
    ax.annotate(r"$P_{\mathrm{A}}^{\mathrm{R}}=x_{\mathrm{A}}P_{\mathrm{A}}^*$", (xb, pr), xytext=(8, -18 if W > 0 else 6), textcoords="offset points", color="tab:blue", fontsize=13)
    ax.text(0.03, 0.08, "Raoult's law", color="tab:blue", fontsize=12, rotation=0)
    ax.plot(0, PA, "o", color="tab:orange", ms=8, clip_on=False, zorder=5)
    ax.set_ylim(0, 1.1); frame(ax, "Pressure of A [bar]", left=(PA, r"$P_{\mathrm{A}}^*$")); ax.set_title(title, fontsize=15)
save(fig, f"{out}/ch13_activity.png")

# colligative properties: mu-T with the solution line
fig, ax = plt.subplots(figsize=(7.5, 5))
ax.plot(T, mu_s(T), color="k", lw=2); ax.plot(T, mu_g0(T), color="k", lw=2)
ax.plot(T, mu_l(T), color="0.6", lw=2)
lower = -3.0   # schematic lowering of the chemical potential of the solvent, RT ln x
sol = lambda T: mu_l(T) + lower
ax.plot(T, sol(T), color="tab:purple", lw=2.5)
tm0, tb0 = brentq(lambda t: mu_s(t) - mu_l(t), 200, 360), brentq(lambda t: mu_l(t) - mu_g0(t), 280, 465)
tm1, tb1 = brentq(lambda t: mu_s(t) - sol(t), 200, 360), brentq(lambda t: sol(t) - mu_g0(t), 280, 465)
for t, c in [(tm0, "0.6"), (tb0, "0.6"), (tm1, "tab:green"), (tb1, "tab:blue")]:
    ax.axvline(t, ls=":", color=c)
ax.text(T[-1] + 4, mu_s(T[-1]), "solid", fontsize=14, va="center"); ax.text(T[-1] + 4, mu_g0(T[-1]), "gas", fontsize=14, va="center")
ax.text(T[-1] + 4, mu_l(T[-1]), "pure solvent", fontsize=13, color="0.5", va="center"); ax.text(T[-1] + 4, sol(T[-1]), "solution", fontsize=13, color="tab:purple", va="center")
ax.annotate("", xy=(tm1, -36), xytext=(tm0, -36), arrowprops=dict(arrowstyle="->", color="tab:green", lw=2))
ax.text(tm1 - 5, -33, "melting point\ndecrease", color="tab:green", fontsize=11, ha="right")
ax.annotate("", xy=(tb1, -36), xytext=(tb0, -36), arrowprops=dict(arrowstyle="->", color="tab:blue", lw=2))
ax.text(tb1 + 5, -33, "boiling point\nincrease", color="tab:blue", fontsize=11, ha="left")
ax.set_xlabel("$T$"); ax.set_ylabel(r"$\mu$ of the solvent"); ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(-42, 12); ax.set_xlim(175, 560)
save(fig, f"{out}/ch13_colligative.png")
