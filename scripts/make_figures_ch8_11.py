"""Computed figures for chapters 8-11. Usage: python3 scripts/make_figures_ch8_11.py img"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from figstyle import save, PURPLE

out = sys.argv[1] if len(sys.argv) > 1 else "img"
R = 0.08314  # L bar / (mol K)

# ---------- ch. 8: A and G decrease to a minimum ----------
fig, axs = plt.subplots(1, 2, figsize=(10, 4))
t = np.linspace(0, 5, 300)
for ax, col, lab, cond in [(axs[0], "tab:red", "Helmholtz energy, $A$", "constant $T,V$"),
                           (axs[1], "tab:blue", "Gibbs energy, $G$", "constant $T,P$")]:
    ax.plot(t, 1 + 2 * np.exp(-1.2 * t), color=col, lw=2.5)
    ax.axhline(1, ls=":", color="gray")
    ax.text(4.9, 1.08, "equilibrium", ha="right", color="gray", fontsize=13)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel("time"); ax.set_ylabel(lab)
    ax.set_title(cond, fontsize=15); ax.set_ylim(0.8, 3.2)
save(fig, f"{out}/ch8_AG_minimum.png")

# ---------- ch. 9: G of liquid and gaseous ethanol vs pressure at 310 K ----------
T = 310.0; Rk = 8.314e-3
G_l0 = -174.0                      # kJ/mol, liquid (nearly flat)
Pvap = 0.15                         # bar
G_g0 = G_l0 - Rk * T * np.log(Pvap)  # so that the curves cross at Pvap
Vl = 0.0584 * 1e-2                 # kJ/(mol bar): 58.4 mL/mol = 0.0584 L/mol = 0.00584 kJ/bar... (1 L bar = 0.1 kJ)
Vl = 0.0584 * 0.1
Pp = np.linspace(0.005, 10, 600)
fig, ax = plt.subplots(figsize=(7.5, 4.8))
ax.plot(Pp, G_g0 + Rk * T * np.log(Pp), color="tab:blue", lw=2.5, label="gas")
ax.plot(Pp, G_l0 + Vl * (Pp - 1), color="k", lw=2.5, label="liquid")
ax.plot(Pvap, G_l0, "o", color=PURPLE, ms=9, zorder=5)
ax.annotate(r"$P^*_{\mathrm{vap}}=0.15$ bar", (Pvap, G_l0), xytext=(25, -40), textcoords="offset points",
            color=PURPLE, arrowprops=dict(arrowstyle="->", color=PURPLE))
ax.text(8, -162.5, "gas", color="tab:blue"); ax.text(8, -173.4, "liquid")
ax.text(0.3, -160.7, r"1 mol of C$_2$H$_5$OH, $T=310$ K", fontsize=14)
ax.set_xlim(0, 10); ax.set_ylim(-180, -159)
ax.set_xlabel("Pressure [bar]"); ax.set_ylabel(r"$\Delta_{\mathrm{f}}G$ [kJ/mol]")
save(fig, f"{out}/ch9_G_vs_P_ethanol.png")

# ---------- ch. 10: van 't Hoff plots ----------
fig, axs = plt.subplots(1, 2, figsize=(10, 4))
x = np.linspace(0, 1, 50)
for ax, slope, col, title in [(axs[0], -1, "tab:blue", "endothermic, $\\Delta H^{\\ominus}>0$"),
                              (axs[1], 1, "tab:red", "exothermic, $\\Delta H^{\\ominus}<0$")]:
    y = 0.5 + slope * 0.6 * (x - 0.5)
    ax.plot(x, y, color=col, lw=2.5)
    for xi, lab in [(0.15, "1"), (0.85, "2")]:
        yi = 0.5 + slope * 0.6 * (xi - 0.5); ax.plot(xi, yi, "o", color=PURPLE, ms=8)
        ax.annotate(lab, (xi, yi), xytext=(6, 6), textcoords="offset points", color=PURPLE)
    ax.text(0.5 if slope < 0 else 0.62, 0.1, r"slope $=-\Delta H^{\ominus}/R$", ha="center", fontsize=14, color="0.3")
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel("$1/T$"); ax.set_ylabel(r"$\ln K$")
    ax.set_title(title, fontsize=15); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
save(fig, f"{out}/ch10_vanthoff.png")

# ---------- ch. 11: ideal gas laws ----------
fig, ax = plt.subplots(figsize=(7, 4.6))
V = np.linspace(0.02, 1.25, 400)
for Tk, lab, yoff in [(300, "$T_1$", 0), (900, "$T_2>T_1$", 0)]:
    ax.plot(V, R * Tk / V, lw=2.5, color="tab:blue" if Tk == 300 else "tab:red")
ax.text(0.55, R * 300 / 0.55 + 10, "$T_1$", color="tab:blue"); ax.text(0.55, R * 900 / 0.55 + 8, "$T_2>T_1$", color="tab:red")
ax.set_ylim(0, 600); ax.set_xlim(0, 1.25); ax.set_xlabel("Volume [L]"); ax.set_ylabel("Pressure [bar]")
ax.set_title("1 mol, constant $T$ (isotherms)", fontsize=15)
save(fig, f"{out}/ch11_PV_ideal.png")

tc = np.linspace(-273.15, 200, 300)


def lin_plot(path, vals, ylabel, title, unit_lab, colors, labels):
    fig, ax = plt.subplots(figsize=(7, 4.6))
    for v, col, lab in zip(vals, colors, labels):
        y = R * (tc + 273.15) / v
        ax.plot(tc, y, lw=2.5, color=col, label=lab)
        y0 = R * 273.15 / v
        ax.plot(0, y0, "o", color=col, ms=7, zorder=5)
        ax.annotate(f"{y0:.1f} {unit_lab}", (0, y0), xytext=(8, -18), textcoords="offset points", color=col, fontsize=12)
    ax.plot(-273.15, 0, "o", color=PURPLE, ms=8, clip_on=False, zorder=5)
    ax.set_xlabel(r"Temperature [$^\circ$C]"); ax.set_ylim(0, 45); ax.set_xlim(-280, 200)
    # y axis drawn at 0 degC, with its label written horizontally at the top of the axis;
    # absolute zero marked as a purple tick label below the x axis
    ax.spines["left"].set_position(("data", 0))
    ax.set_yticks([10, 20, 30, 40]); ax.set_yticklabels([])
    for yt in [10, 20, 30, 40]:  # tick labels on a white background, so the lines do not run through them
        ax.text(-7, yt, str(yt), ha="right", va="center", zorder=10, bbox=dict(fc="white", ec="none", pad=1))
    ax.text(8, 45, ylabel, va="top", ha="left")
    ax.set_xticks([-273.15, -100, 0, 100, 200])
    ax.set_xticklabels(["\u2212273.15", "\u2212100", "0", "100", "200"])
    ax.get_xticklabels()[0].set_color(PURPLE); ax.get_xticklines()[0].set_color(PURPLE)
    ax.legend(frameon=False, loc="upper left"); ax.set_title(title, fontsize=15)
    save(fig, path)


lin_plot(f"{out}/ch11_VT_ideal.png", [1.0, 2.0], "Volume [L]", "1 mol, constant $P$ (isobars)", "L",
         ["tab:green", "darkgreen"], [r"$P_1=1$ bar", r"$P_2=2$ bar $>P_1$"])
lin_plot(f"{out}/ch11_PT_ideal.png", [1.0, 2.0], "Pressure [bar]", "1 mol, constant $V$ (isochors)", "bar",
         ["tab:orange", "saddlebrown"], [r"$V_1=1$ L", r"$V_2=2$ L $>V_1$"])

# Avogadro's law
fig, ax = plt.subplots(figsize=(7, 4.6))
nn = np.linspace(0, 3, 50)
for Tk, col in [(273.15, "tab:blue"), (373.15, "tab:red")]:
    ax.plot(nn, nn * R * Tk / 1.0, lw=2.5, color=col, label=f"$T={Tk:.0f}$ K")
ax.plot(1, R * 273.15, "o", color=PURPLE, ms=8, zorder=5)
ax.plot([1, 1], [0, R * 273.15], ":", color=PURPLE, lw=2)
ax.annotate(f"1 mol: {R*273.15:.1f} L", (1, R * 273.15), xytext=(15, -25), textcoords="offset points", color=PURPLE, fontsize=13)
ax.set_xlabel("Number of moles, $n$ [mol]"); ax.set_ylabel("Volume [L]"); ax.set_xlim(0, 3); ax.set_ylim(0, 100)
ax.legend(frameon=False, loc="upper left"); ax.set_title("constant $P=1$ bar", fontsize=15)
save(fig, f"{out}/ch11_V_n_ideal.png")


# ---------- ch. 11: van der Waals compressibility factors ----------
gases = {"H$_2$": (0.2476, 0.02661), "CO$_2$": (3.640, 0.04267)}


def vdw_V(P, T, a, b):
    """Molar volume of the gas-like root of the vdW equation."""
    roots = np.roots([P, -(P * b + R * T), a, -a * b])
    real = roots[np.abs(roots.imag) < 1e-9].real
    return real.max()


Pgrid = np.linspace(0.5, 600, 300)
fig, ax = plt.subplots(figsize=(7.5, 4.8))
for (name, (a, b)), col in zip(gases.items(), ["tab:blue", "tab:red"]):
    z = [p * vdw_V(p, 350, a, b) / (R * 350) for p in Pgrid]
    ax.plot(Pgrid, z, color=col, lw=2.5)
    ax.text(Pgrid[-1] * 0.98, z[-1] - 0.2 if "H" in name else 0.88, ("Type I (" if "H" in name else "Type II (") + name + ")", color=col, ha="right")
ax.axhline(1, ls=":", color="k"); ax.text(250, 0.95, "ideal gas", fontsize=13)
ax.set_xlim(0, 600); ax.set_xlabel("Pressure [bar]"); ax.set_ylabel("$z$"); ax.set_title("van der Waals gases at 350 K", fontsize=15, pad=12)
save(fig, f"{out}/ch11_z_vs_P.png")

fig, axs = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
TB_CO2 = 3.640 / (0.04267 * R)
for ax, (name, (a, b)), temps in zip(axs, gases.items(), [(200, 500, 1000), (350, 500, TB_CO2, 2000)]):
    cols = plt.cm.plasma(np.linspace(0.1, 0.8, len(temps)))
    for Tk, c in zip(temps, cols):
        z = [p * vdw_V(p, Tk, a, b) / (R * Tk) for p in Pgrid]
        isB = name.startswith("CO") and Tk == TB_CO2
        ax.plot(Pgrid, z, color=c, lw=3 if isB else 1.8,
                label=(r"$T_{\mathrm{B}}$" + f" = {Tk:.0f} K") if isB else f"{Tk:.0f} K")
    ax.axhline(1, ls=":", color="k"); ax.set_xlabel("Pressure [bar]"); ax.set_xlim(0, 600)
    ax.legend(fontsize=12, frameon=False, loc="upper left")
    ax.set_title(("Type I: " if "H" in name else "Type II: ") + name, fontsize=15)
axs[0].set_ylabel("$z$"); axs[0].set_ylim(0.4, 1.8)
save(fig, f"{out}/ch11_z_vs_T.png")


# ---------- ch. 11: van der Waals isotherms with the liquid-vapor dome (reduced units) ----------
def p_r(v, t):
    return 8 * t / (3 * v - 1) - 3 / v ** 2


def maxwell(t):
    """Coexistence pressure and volumes for reduced temperature t<1 (equal-area construction)."""
    def area(p):
        roots = np.sort(np.roots([3 * p, -(p + 8 * t), 9, -3]).real)
        vl, vg = roots[0], roots[-1]
        integ = (8 * t / 3) * np.log((3 * vg - 1) / (3 * vl - 1)) + 3 / vg - 3 / vl
        return integ - p * (vg - vl), vl, vg
    vs = np.linspace(0.34, 6, 20000); ps = p_r(vs, t)
    d = np.diff(ps); ext = np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0] + 1
    pmin, pmax = max(ps[ext[0]], 1e-4), ps[ext[1]]
    p = brentq(lambda q: area(q)[0], pmin + 1e-6, pmax - 1e-6)
    return p, area(p)[1], area(p)[2]


tdome = np.linspace(0.8, 0.9999, 80)
dome = [maxwell(t) for t in tdome]
vl_d = [d[1] for d in dome]; vg_d = [d[2] for d in dome]; p_d = [d[0] for d in dome]
fig, ax = plt.subplots(figsize=(7.5, 5))
dv = np.concatenate([vl_d, [1.0], vg_d[::-1]]); dp = np.concatenate([p_d, [1.0], p_d[::-1]])
ax.fill(dv, dp, color="tab:green", alpha=0.25)
ax.plot(dv, dp, color="tab:green", lw=2)
vv = np.linspace(0.42, 4.5, 800)
for t, lab in [(0.88, "$T_1$"), (0.94, "$T_2$"), (1.0, "$T_c$"), (1.08, "$T_3$"), (1.2, "$T_4$"), (1.4, "$T_5$")]:
    pp = p_r(vv, t)
    if t < 1:
        p0, vl0, vg0 = maxwell(t)
        pp = np.where((vv > vl0) & (vv < vg0), p0, pp)
    ax.plot(vv, pp, color="k" if t == 1.0 else "tab:blue", lw=2.2 if t == 1.0 else 1.6)
    # labels spread out vertically at the right end, each joined to its own isotherm by a short leader line
    ylab = {0.88: 0.415, 0.94: 0.50, 1.0: 0.585, 1.08: 0.67, 1.2: 0.755, 1.4: 0.84}[t]
    col = "k" if t == 1.0 else "tab:blue"
    ax.plot([4.5, 4.62, 4.75], [p_r(4.5, t), ylab, ylab], color=col, lw=0.8)
    ax.text(4.78, ylab, lab, va="center", fontsize=13, color=col)
ax.plot(1, 1, "o", color="tab:red", ms=9); ax.annotate("critical point", (1, 1), xytext=(6, 6), textcoords="offset points", color="tab:red")
ax.text(0.55, 0.985, "liquid", fontsize=14, ha="center", va="center", bbox=dict(fc="white", ec="none", alpha=0.8, pad=1)); ax.text(1.3, 0.48, "liquid + vapor", fontsize=14)
ax.text(3.1, 0.55, "vapor", fontsize=13, bbox=dict(fc="white", ec="none", alpha=0.8, pad=1)); ax.text(1.75, 1.45, "gas", fontsize=14, ha="center", va="center", bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
ax.set_xlim(0.3, 5.1); ax.set_ylim(min(p_d), 2.0)
ax.set_xlabel(r"Volume, $\overline{V}/\overline{V}_c$"); ax.set_ylabel(r"Pressure, $P/P_c$")
save(fig, f"{out}/ch11_vdw_isotherms.png")

