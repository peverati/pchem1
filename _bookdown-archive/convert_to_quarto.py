"""Convert the bookdown chapters of the Live Textbook of P-Chem 1 to Quarto (.qmd).

Usage (from the project root):  python3 _bookdown-archive/convert_to_quarto.py
Reads the .Rmd sources in _bookdown-archive/ and writes .qmd files into the project root.
R plot chunks are evaluated once with Rscript and saved as PNG files in img/,
so the converted book no longer needs R. The original sources are not modified.

Adapted from the P-Chem 2 converter (pchem2/_bookdown-archive/convert_to_quarto.py).
"""
import re
import os
import subprocess
import tempfile
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
# (source file, output file, old bookdown page name for the alias)
CHAPTERS = [
    ("01_Basis.rmd", "01_Basis.qmd", "SystemVariables"),
    ("02_ZerothLaw.rmd", "02_ZerothLaw.qmd", "ZerothLaw"),
    ("03_FirstLaw.rmd", "03_FirstLaw.qmd", "FirstLaw"),
    ("04_Thermochemistry.Rmd", "04_Thermochemistry.qmd", "Thermochemistry"),
    ("05_ThermodynamicCycles.Rmd", "05_ThermodynamicCycles.qmd", "ThermodynamicCycles"),
    ("06_SecondLaw.Rmd", "06_SecondLaw.qmd", "SecondLaw"),
    ("07_ThirdLaw.Rmd", "07_ThirdLaw.qmd", "thirdlaw"),
    ("08_Potentials.Rmd", "08_Potentials.qmd", "Potentials"),
    ("09_Gibbs.Rmd", "09_Gibbs.qmd", "GibbsFree"),
    ("10_ChemicalEquilibrium.Rmd", "10_ChemicalEquilibrium.qmd", "ChemicalEquilibrium"),
    ("11_NonIdealGases.Rmd", "11_NonIdealGases.qmd", "RealGases"),
    ("12_PhaseEquilibrium.Rmd", "12_PhaseEquilibrium.qmd", "PhaseEquilibrium"),
    ("13_MCPhaseDiagrams.Rmd", "13_MCPhaseDiagrams.qmd", "MCPhaseDiagrams"),
    ("15_Kinetics.Rmd", "15_Kinetics.qmd", "Kinetics"),
    ("16_Appendix.Rmd", "A1_Appendix.qmd", "appendix"),
]

warnings = []


def r_unescape(s):
    """Undo R string escaping inside fig.cap / fig.alt."""
    return s.replace("\\'", "'").replace('\\"', '"').replace("\\\\", "\\")


def opt(header, name):
    """Chunk option value, in single or double quotes."""
    m = re.search(re.escape(name) + r"\s*=\s*'((?:[^'\\]|\\.)*)'", header) or \
        re.search(re.escape(name) + r'\s*=\s*"((?:[^"\\]|\\.)*)"', header)
    return r_unescape(m.group(1)) if m else None


def num_opt(header, name):
    m = re.search(re.escape(name) + r"\s*=\s*([0-9.]+)", header)
    return float(m.group(1)) if m else None


def image_md(prefix, cap, path, label, alt, width):
    attrs = []
    if label and cap is not None:
        attrs.append(f"#fig-{label}")
    if alt:
        attrs.append('fig-alt="' + alt.replace('"', "&quot;") + '"')
    else:
        warnings.append(f"figure without alt text: {path}")
    if width:
        attrs.append(f'width="{width}"')
    return f"{prefix}\n{prefix}![{cap or ''}]({path}){{{' '.join(attrs)}}}\n{prefix}"


class ChunkConverter:
    """Turns ```{r} chunks into Markdown images; runs plotting code once with R."""

    def __init__(self, stem):
        self.stem = stem
        self.n = 0

    def __call__(self, m):
        prefix, header, code = m.group(1) or "", m.group(2), m.group(3)
        code = re.sub(r"(?m)^> ?", "", code) if prefix else code
        label = re.match(r"\{r[ ,]+([A-Za-z0-9_]+)\s*[,}]", header)
        label = label.group(1) if label and "=" not in label.group(1) else None
        cap, alt, width = opt(header, "fig.cap"), opt(header, "fig.alt"), opt(header, "out.width")
        inc = re.fullmatch(r"\s*knitr::include_graphics\(['\"]([^'\"]+)['\"]\)\s*", code)
        if inc:
            return image_md(prefix, cap, inc.group(1).replace("./", ""), label, alt, width)
        # plotting chunk: evaluate once with R and save a PNG
        self.n += 1
        name = f"img/R_{self.stem}_{label or self.n}.png"
        fw = num_opt(header, "fig.width") or 7
        asp = num_opt(header, "fig.asp")
        fh = num_opt(header, "fig.height") or (fw * asp if asp else 5)
        script = (f"png('{ROOT / name}', width={fw}, height={fh}, units='in', res=200)\n"
                  f"{code}\ninvisible(dev.off())\n")
        with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False) as f:
            f.write(script)
        res = subprocess.run(["Rscript", f.name], capture_output=True, text=True, cwd=ROOT)
        os.unlink(f.name)
        if res.returncode != 0:
            warnings.append(f"R plot {name}: {res.stderr.strip()}")
            return m.group(0)
        return image_md(prefix, cap, name, label, alt, width)


def convert_answers(m):
    ans = m.group(1).strip()
    return ('::: {.callout-tip collapse="true" icon="false"}\n## Answers\n\n' + ans + "\n:::")


def convert_block(m):
    """bookdown theorem-like blocks (definition, exercise) -> Quarto cross-referenceable divs."""
    kind, label, body = m.group(1), m.group(2), m.group(3)
    body = re.sub(r"(?m)^> ?", "", body)
    if body.count("```") % 2:      # a figure chunk inside the block shares the block's closing fence
        body += "\n```"
    pre = {"definition": "def", "exercise": "exr", "example": "exm"}[kind]
    return f"::: {{#{pre}-{label}}}\n{body.strip()}\n:::"


PREFIX_WORDS = {
    "eq": r"(?:[Ee]qs?\.|[Ee]quations?)\s+",
    "fig": r"(?:[Ff]igures?)\s+",
    "tab": r"(?:[Tt]ables?)\s+",
    "def": r"(?:[Dd]efinitions?)\s+",
    "exr": r"(?:[Ee]xercises?)\s+",
    "sec": r"(?:[Cc]hapters?|[Ss]ections?|[Aa]ppendix)\s+",
}


def convert_refs(text):
    # typed references with a preceding word ("eq. \@ref(eq:x)" -> "@eq-x"; capitalized if the word was)
    for kind, qkind in (("eq", "eq"), ("fig", "fig"), ("tab", "tbl"), ("def", "def"), ("exr", "exr")):
        def repl(m, qkind=qkind):
            cap = m.group(1)[0].isupper() if m.group(1) else False
            pre = qkind[0].upper() + qkind[1:] if cap else qkind
            ref = f"@{pre}-{m.group(2)}"
            nxt = m.string[m.end():m.end() + 1]
            return f"[{ref}]" if nxt.isalnum() else ref
        text = re.sub(r"(" + PREFIX_WORDS[kind] + r")?\\@ref\(" + kind + r":([A-Za-z0-9_\-]+)\)", repl, text)

    # section / chapter references
    def srepl(m):
        cap = m.group(1)[0].isupper() if m.group(1) else False
        ref = f"@{'Sec' if cap else 'sec'}-{m.group(2)}"
        nxt = m.string[m.end():m.end() + 1]
        return f"[{ref}]" if nxt.isalnum() else ref
    text = re.sub(r"(" + PREFIX_WORDS["sec"] + r")?\\@ref\(([A-Za-z0-9_\-]+)\)", srepl, text)
    return text


def modernize_math(s):
    """Replace old LaTeX idioms that newer engines (e.g., Typst via Pandoc) cannot convert."""
    s = re.sub(r"\{\\bf\s*([^{}]+?)\}", r"\\mathbf{\1}", s)
    s = re.sub(r"\{\\cal\s*([^{}]+?)\}", r"\\mathcal{\1}", s)
    s = re.sub(r"\\hat\\mathbf\{([^{}]+)\}", r"\\hat{\\mathbf{\1}}", s)
    s = s.replace("\\begin{vmatrix}", "\\left|\\begin{matrix}").replace("\\end{vmatrix}", "\\end{matrix}\\right|")
    s = re.sub(r"(?m)^\$\\\\\$\s*$", "", s)        # lines containing only $\\$ (spacing hack)
    # MathJax 4 fails on an arrow labeled only with a space, and on this mhchem arrow (the only \ce in the book)
    s = s.replace("\\xrightarrow{\\quad}", "\\xrightarrow{\\hphantom{k_n}}")
    s = s.replace("\\ce{<=>[k_1][k_{-1}]}", "\\underset{k_{-1}}{\\overset{k_1}{\\rightleftharpoons}}")
    return s


def convert(src, stem):
    s = src
    # LaTeX-only lines: macro definitions (now global, in _quarto.yml / mathjax-macros.html) and page control
    s = re.sub(r"(?m)^\\(re)?newcommand\*?\{\\standardstate\}.*\n", "", s)
    s = re.sub(r"(?m)^\\(cleardoublepage|pagenumbering\{arabic\})\s*\n", "", s)
    s = modernize_math(s)
    # definition / exercise blocks
    s = re.sub(r"(?ms)^> ?```\{(definition|exercise|example),\s*([A-Za-z0-9_\-]+)[^}]*\}[ \t]*\n(.*?)\n> ?```[ \t]*$",
               convert_block, s)
    # R chunks: figures (include_graphics) and plots (evaluated with R); optionally inside a blockquote
    s = re.sub(r"(?ms)^(> ?)?```(\{r[^\n]*\})\n(.*?)\n(?:> ?)?```[ \t]*$", ChunkConverter(stem), s)
    # answer reveal blocks: keep the text of the LaTeX branch
    s = re.sub(r"`r if \(knitr::is_html_output\(\)\) \{.*?is_latex_output\(\)\) \{\s*'Answers:\s*(.*?)\s*'\s*\}`",
               convert_answers, s, flags=re.S)
    # equations: \begin{equation} body (\#eq:label) \end{equation}  ->  $$ body $$ {#eq-label}
    def eq(m):
        body = m.group(1).rstrip()
        lab = re.search(r"\(\\#eq:([A-Za-z0-9_\-]+)\)", body)
        body = re.sub(r"\s*\(\\#eq:[A-Za-z0-9_\-]+\)\s*", "\n", body).strip()
        return "$$\n" + body + "\n$$" + (f" {{#eq-{lab.group(1)}}}" if lab else "")
    s = re.sub(r"\\begin\{equation\}\s*\n?(.*?)\\end\{equation\}", eq, s, flags=re.S)
    # headers: {#Label} -> {#sec-Label}; {-} -> {.unnumbered}
    s = re.sub(r"(?m)^(#+ .*?)\s*\{#([A-Za-z0-9_\-]+)\}\s*\{-\}\s*$", r"\1 {#sec-\2 .unnumbered}", s)
    s = re.sub(r"(?m)^(#+ .*?)\s*\{-\}\s*$", r"\1 {.unnumbered}", s)
    s = re.sub(r"(?m)^(#+ .*?)\s*\{#([A-Za-z0-9_\-]+)\}\s*$", r"\1 {#sec-\2}", s)
    s = convert_refs(s)
    for left in re.findall(r"\\@ref\([^)]*\)", s):
        warnings.append(f"{stem}: {left}")
    if "knitr::" in s or "```{" in s or "`r " in s:
        warnings.append(f"{stem}: leftover R chunk or knitr call")
    return s


def main():
    for src, out, alias in CHAPTERS:
        stem = Path(out).stem
        body = convert((SRC / src).read_text(), stem)
        front = f"---\naliases:\n  - {alias}.html\n---\n\n"
        (ROOT / out).write_text(front + body.lstrip("\n"))
    idx = (SRC / "index.Rmd").read_text()
    idx = idx.split("---", 2)[2]  # drop YAML (moved to _quarto.yml)
    idx = idx.replace("\\renewcommand{\\arraystretch}{1.8}\n", "")
    (ROOT / "index.qmd").write_text(convert(idx, "index").lstrip("\n"))
    print("converted", len(CHAPTERS), "chapters;", len(warnings), "warnings")
    for w in sorted(set(warnings)):
        print("  ", w)


if __name__ == "__main__":
    sys.exit(main())
