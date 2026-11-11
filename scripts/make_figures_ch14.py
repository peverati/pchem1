"""Figures for chapter 14 (kinetics). Usage: python3 scripts/make_figures_ch14.py img"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from figstyle import save, PURPLE

out = sys.argv[1] if len(sys.argv) > 1 else "img"
A0 = 1.6
t = np.linspace(0, 4, 300)


def simple(path, y, ylabel, title, slope_lab, col):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(t, y, color=col, lw=2.5)
    ax.set_xlabel("$t$"); ax.set_ylabel(ylabel); ax.set_title(title, fontsize=15)
    ax.set_xlim(0, 4); ax.set_ylim(min(0, y.min() * 1.1), max(2.0, y.max() * 1.1))
    if slope_lab:
        k = 120; ax.annotate(slope_lab, (t[k], y[k]), xytext=(30, -45 if "+" in slope_lab else 20), textcoords="offset points",
                             color=PURPLE, fontsize=16, arrowprops=dict(arrowstyle="->", color=PURPLE))
    save(fig, path)


k0, k1, k2 = 0.4, 0.8, 0.4
simple(f"{out}/ch14_zeroth.png", np.clip(A0 - k0 * t, 0, None), r"$[\mathrm{A}]$", "zeroth-order reaction", r"slope $=-k_0$", "tab:blue")
simple(f"{out}/ch14_first.png", A0 * np.exp(-k1 * t), r"$[\mathrm{A}]$", "first-order reaction", None, "tab:blue")
simple(f"{out}/ch14_first_lin.png", np.log(A0 * np.exp(-k1 * t)), r"$\ln[\mathrm{A}]$", "first-order reaction", r"slope $=-k_1$", "tab:green")
simple(f"{out}/ch14_second_lin.png", 1 / A0 + k2 * t, r"$1/[\mathrm{A}]$", "second-order reaction", r"slope $=+k_2$", "tab:orange")

tt = np.linspace(0, 100, 500)


def conc_plot(path, curves, title):
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    for y, lab, col in curves:
        ax.plot(tt, y, color=col, lw=2.5, label=lab)
    ax.set_xlabel("$t$ [s]"); ax.set_ylabel(r"$[\mathrm{X}]/[\mathrm{A}]_0$"); ax.set_ylim(0, 1.05); ax.set_xlim(0, 100)
    ax.legend(frameon=False, loc="center right"); ax.set_title(title, fontsize=15)
    return fig, ax


def consecutive(k1, k2):
    A = np.exp(-k1 * tt); B = k1 / (k2 - k1) * (np.exp(-k1 * tt) - np.exp(-k2 * tt))
    return A, B, 1 - A - B


A, B, C = consecutive(0.08, 0.04)
fig, ax = conc_plot(f"{out}/ch14_consecutive_slow2.png", [(A, "[A]", "tab:blue"), (B, "[B]", "tab:red"), (C, "[C]", "tab:green")],
                    r"$k_1=0.08\;\mathrm{s^{-1}}$, $k_2=0.04\;\mathrm{s^{-1}}$ (second step slower)")
save(fig, f"{out}/ch14_consecutive_slow2.png")
A, B, C = consecutive(0.08, 2.0)
fig, ax = conc_plot(f"{out}/ch14_consecutive_slow1.png", [(A, "[A]", "tab:blue"), (B, "[B]", "tab:red"), (C, "[C]", "tab:green")],
                    r"$k_1=0.08\;\mathrm{s^{-1}}$, $k_2=2.0\;\mathrm{s^{-1}}$ (first step slower)")
save(fig, f"{out}/ch14_consecutive_slow1.png")

k1c, k2c = 0.04, 0.02
A = np.exp(-(k1c + k2c) * tt); B = k1c / (k1c + k2c) * (1 - A); C = k2c / (k1c + k2c) * (1 - A)
fig, ax = conc_plot("", [(A, "[A]", "tab:blue"), (B, "[B]", "tab:red"), (C, "[C]", "tab:green")],
                    r"competitive: $k_1=0.04\;\mathrm{s^{-1}}$, $k_2=0.02\;\mathrm{s^{-1}}$")
save(fig, f"{out}/ch14_competitive.png")

kf, kr = 0.1, 0.05
A = (kr + kf * np.exp(-(kf + kr) * tt)) / (kf + kr); B = 1 - A
fig, ax = conc_plot("", [(A, "[A]", "tab:blue"), (B, "[B]", "tab:red")],
                    r"opposed: $k_1=0.1\;\mathrm{s^{-1}}$, $k_{-1}=0.05\;\mathrm{s^{-1}}$")
ax.axhline(kr / (kf + kr), ls=":", color="tab:blue"); ax.axhline(kf / (kf + kr), ls=":", color="tab:red")
ax.text(60, kf / (kf + kr) + 0.03, r"$[\mathrm{B}]_{\mathrm{eq}}/[\mathrm{A}]_{\mathrm{eq}}=K_C=k_1/k_{-1}=2$", fontsize=13)
save(fig, f"{out}/ch14_opposed.png")

# Arrhenius plot
fig, ax = plt.subplots(figsize=(7, 4.5))
x = np.linspace(0, 1, 50); y = 0.9 - 0.7 * x
ax.plot(x, y, color="tab:blue", lw=2.5)
for xi, lab in [(0.25, "1"), (0.75, "2")]:
    yi = 0.9 - 0.7 * xi; ax.plot(xi, yi, "o", color=PURPLE, ms=9)
    ax.annotate(lab, (xi, yi), xytext=(6, 8), textcoords="offset points", color=PURPLE)
    ax.plot([xi, xi], [0, yi], ":", color="gray")
ax.set_xticks([0.25, 0.75]); ax.set_xticklabels([r"$1/T_1$", r"$1/T_2$"]); ax.set_yticks([])
ax.text(0.45, 0.65, r"slope $=-E_a/R$", fontsize=15, color="0.3")
ax.set_xlabel("$1/T$"); ax.set_ylabel(r"$\ln k$"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
save(fig, f"{out}/ch14_arrhenius.png")

# reaction coordinate diagram
s = np.linspace(0, 1, 400)
E = 0.0 * (1 - s) - 0.45 * s / (1 + np.exp(-(s - 0.5) * 12)) * 2 / (1 + np.exp(-6)) * 0 + 1.0 * np.exp(-((s - 0.45) / 0.12) ** 2)
E = E - 0.5 / (1 + np.exp(-(s - 0.55) * 14))
fig, ax = plt.subplots(figsize=(7.5, 5))
ax.plot(s, E, color="k", lw=2.5)
i_ts = np.argmax(E); Ets = E[i_ts]; Er = E[0]; Ep = E[-1]
ax.axhline(Er, xmax=0.35, ls=":", color="gray"); ax.axhline(Ep, xmin=0.7, ls=":", color="gray")
ax.annotate("", xy=(0.2, Ets), xytext=(0.2, Er), arrowprops=dict(arrowstyle="<->", color=PURPLE, lw=2))
ax.plot([0.2, s[i_ts]], [Ets, Ets], ":", color="gray")
ax.text(0.22, (Ets + Er) / 2, r"$E_a$", color=PURPLE, fontsize=17)
ax.annotate("", xy=(0.88, Ep), xytext=(0.88, Er), arrowprops=dict(arrowstyle="<->", color="tab:blue", lw=2))
ax.plot([0.35, 0.88], [Er, Er], ":", color="gray")
ax.text(0.9, (Er + Ep) / 2, r"$\Delta_{\mathrm{rxn}}H$", color="tab:blue", fontsize=15)
ax.text(s[i_ts], Ets + 0.05, "transition state", ha="center", fontsize=14)
ax.text(0.02, Er + 0.05, "reactants", fontsize=14); ax.text(0.78, Ep - 0.12, "products", fontsize=14)
ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel("reaction coordinate"); ax.set_ylabel("energy")
ax.set_ylim(Ep - 0.25, Ets + 0.2)
save(fig, f"{out}/ch14_reaction_coordinate.png")
