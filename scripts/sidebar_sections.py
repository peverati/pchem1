"""Quarto post-render step: collect the table of contents of every page into
sidebar-sections.json, used by sidebar-toc.html to list each chapter's sections
in the left sidebar (expandable with an arrow).
"""
import json
import os
import re
from pathlib import Path


SYMBOLS = {r"\rightleftarrows": "\u21c4", r"\rightarrow": "\u2192", r"\neq": "\u2260", r"\Delta": "\u0394", r"\;": " ", r"\,": " "}


def plain_math(tex):
    """Turn the simple inline math used in headings into HTML text (italic symbols, sub/superscripts),
    so the sidebar does not depend on MathJax. Returns None if something is not recognized."""
    t = tex.strip()
    t = re.sub(r"\\(?:text|mathrm)\{([^{}]*)\}", lambda m: "\x00" + m.group(1) + "\x01", t)          # upright text, protected
    for k, v in SYMBOLS.items():
        t = t.replace(k, v)
    if "\\" in t:
        return None
    t = re.sub(r"\s*\|\s*", "|", t)
    t = re.sub(r"_\{([^{}]*)\}", r"<sub>\1</sub>", t)
    t = re.sub(r"\^\{([^{}]*)\}", r"<sup>\1</sup>", t)
    t = re.sub(r"_(\w)", r"<sub>\1</sub>", t)
    # italicize single Latin letters (math variables), outside protected upright text and tags
    parts = re.split(r"(\x00[^\x01]*\x01|<[^>]+>)", t)
    parts = [p if p.startswith(("\x00", "<")) else re.sub(r"([A-Za-z])", r"<i>\1</i>", p) for p in parts]
    t = "".join(parts).replace("\x00", "").replace("\x01", "")
    return re.sub(r"\s+", " ", t).replace("\u0394 ", "\u0394")


def replace_math(m):
    txt = plain_math(m.group(1))
    return txt if txt is not None else m.group(0)

out = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs"))
data = {}
for page in sorted(out.glob("*.html")):
    s = page.read_text(encoding="utf-8")
    m = re.search(r'<nav id="TOC"[^>]*>.*?(<ul>.*</ul>)\s*(?:<div class="toc-actions"|</nav>)', s, re.S)
    if not m:
        continue
    ul = m.group(1)
    ul = re.sub(r'\s(id|data-scroll-target)="[^"]*"', "", ul)
    ul = ul.replace(' class="nav-link active"', "").replace(' class="nav-link"', "").replace(' class="collapse"', "")
    ul = re.sub(r'href="#', f'href="{page.name}#', ul)
    ul = re.sub(r'<span class="math inline">\\\((.*?)\\\)</span>', replace_math, ul)
    data[page.name] = ul
(out / "sidebar-sections.json").write_text(json.dumps(data), encoding="utf-8")
print(f"sidebar-sections.json: {len(data)} pages")
