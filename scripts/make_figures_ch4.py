"""Figures for chapters 4 and 5 (Carnot cycle). Usage: python3 scripts/make_figures_ch4.py img"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle
from figstyle import save, PURPLE

out = sys.argv[1] if len(sys.argv) > 1 else "img"
R = 0.08314            # L bar / (mol K)
Th, Tl = 500.0, 350.0  # K
g = 2.0 / 3.0          # T V^(2/3) = const for a monatomic ideal gas
VA, VB = 0.20, 0.30
VC = VB * (Th / Tl) ** 1.5
VD = VA * (Th / Tl) ** 1.5
P = lambda V, T: R * T / V

# ---------- PV diagram of the Carnot cycle ----------
fig, ax = plt.subplots(figsize=(7.5, 5))
V = np.linspace(0.15, 0.62, 400)
ax.plot(V, P(V, Th), color="tab:red", lw=1, alpha=0.4)
ax.plot(V, P(V, Tl), color="tab:blue", lw=1, alpha=0.4)
for Va, Vb, T, col in [(VA, VB, Th, "tab:red"), (VD, VC, Tl, "tab:blue")]:
    v = np.linspace(Va, Vb, 100); ax.plot(v, P(v, T), color=col, lw=3)
for Va, Vb, T0 in [(VB, VC, Th), (VA, VD, Th)]:
    v = np.linspace(Va, Vb, 100); T = T0 * (Va / v) ** g; ax.plot(v, P(v, T), color="0.25", lw=3)
for v, T, lab, off in [(VA, Th, "A", (-18, 6)), (VB, Th, "B", (8, 6)), (VC, Tl, "C", (8, 4)), (VD, Tl, "D", (-20, -16))]:
    ax.plot(v, P(v, T), "o", color=PURPLE, ms=9, zorder=5)
    ax.annotate(lab, (v, P(v, T)), xytext=off, textcoords="offset points", fontsize=17, color=PURPLE)
mid = lambda a, b: (a + b) / 2
ax.text(mid(VA, VB), P(mid(VA, VB), Th) + 6, "1", fontsize=15, color="tab:green")
ax.text(mid(VB, VC) + 0.01, 105, "2", fontsize=15, color="tab:green")
ax.text(mid(VD, VC), P(mid(VD, VC), Tl) + 5, "3", fontsize=15, color="tab:green")
ax.text(mid(VA, VD) - 0.03, 120, "4", fontsize=15, color="tab:green")
ax.text(0.55, P(0.55, Th) + 4, r"isotherm $T_h$", color="tab:red", fontsize=14)
ax.text(0.55, P(0.55, Tl) - 12, r"isotherm $T_l$", color="tab:blue", fontsize=14)
ax.text(0.205, 60, "adiabats", color="0.25", fontsize=14)
ax.set_xlim(0.15, 0.62); ax.set_ylim(30, 230)
ax.set_xlabel("Volume [L]"); ax.set_ylabel("Pressure [bar]")
save(fig, f"{out}/ch4_carnot_pv.png")


# ---------- the four stages ----------
def stage(path, contact, piston_up, particles, heat):
    """contact: 'hot', 'cold' or 'insulated'; heat: 'in', 'out' or None."""
    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.set_xlim(-1.8, 10); ax.set_ylim(0, 8.4); ax.set_aspect("equal"); ax.axis("off")
    base = {"hot": ("#e8665a", r"hot reservoir, $T_h$"), "cold": ("#6fa8dc", r"cold reservoir, $T_l$"),
            "insulated": ("0.75", r"insulation, $Q=0$")}[contact]
    ax.add_patch(Rectangle((0.5, 0.3), 9, 1.4, fc=base[0], ec="0.3", lw=1.5))
    ax.text(5, 1.0, base[1], ha="center", va="center", fontsize=15)
    # cylinder
    ax.plot([3, 3, 7, 7], [6.8, 1.7, 1.7, 6.8], color="0.2", lw=3)
    yp = 5.4 if piston_up else 4.0
    ax.add_patch(Rectangle((3.05, yp), 3.9, 0.35, fc="#a33a2a", ec="0.2"))
    ax.add_patch(Rectangle((4.8, yp + 0.35), 0.4, 6.8 - yp, fc="#a33a2a", ec="0.2"))
    rng = np.random.default_rng(3)
    for _ in range(9):
        ax.add_patch(Circle((rng.uniform(3.4, 6.6), rng.uniform(2.0, yp - 0.3)), 0.17, fc=particles, ec="none"))
    # piston motion
    y0, y1 = (4.2, 5.8) if piston_up else (5.8, 4.2)
    ax.add_patch(FancyArrowPatch((2.2, y0), (2.2, y1), arrowstyle="-|>", mutation_scale=20, lw=2.5, color="0.2"))
    ax.text(1.95, 5.0, "expansion" if piston_up else "compression", fontsize=13, va="center", ha="right")
    if heat:
        a, b = ((7.9, 1.8), (7.9, 3.4)) if heat == "in" else ((7.9, 3.4), (7.9, 1.8))
        lab = r"$|Q_h|$ in" if heat == "in" else r"$|Q_l|$ out"
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=22, lw=3, color=PURPLE))
        ax.text(8.2, 2.6, lab, fontsize=14, color=PURPLE, va="center")
    save(fig, path)


stage(f"{out}/ch4_carnot_stage1.png", "hot", True, "#d62728", "in")
stage(f"{out}/ch4_carnot_stage2.png", "insulated", True, "#9467bd", None)
stage(f"{out}/ch4_carnot_stage3.png", "cold", False, "#1f77b4", "out")
stage(f"{out}/ch4_carnot_stage4.png", "insulated", False, "#9467bd", None)
