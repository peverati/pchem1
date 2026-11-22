"""Figures for chapter 1 (the machine with three knobs). Usage (from the project root): python3 scripts/make_figures_ch1.py img"""
import sys
from machine import draw_machine

out = sys.argv[1] if len(sys.argv) > 1 else "img"
draw_machine(f"{out}/machine_knobs.png", r"$\mathcal{M}=\,$" + "42.0",
             [("a", "$a$", "$da$"), ("b", "$b$", "$db$"), ("c", "$c$", "$dc$")], title="")
