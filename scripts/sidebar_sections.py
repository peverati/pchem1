"""Quarto post-render step: collect the table of contents of every page into
sidebar-sections.json, used by sidebar-toc.html to list each chapter's sections
in the left sidebar (expandable with an arrow).
"""
import json
import os
import re
from pathlib import Path

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
    data[page.name] = ul
(out / "sidebar-sections.json").write_text(json.dumps(data), encoding="utf-8")
print(f"sidebar-sections.json: {len(data)} pages")
