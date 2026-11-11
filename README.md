# The Live Textbook of Physical Chemistry 1

GitHub repository of the Live Textbook of Physical Chemistry 1 by Dr. Peverati, Florida Institute of Technology.

The book is written in Markdown (`.qmd` files) and built with [Quarto](https://quarto.org). R and RStudio are **not** needed.
The previous bookdown version is preserved on the branch `bookdown`.

---

## How to update and rebuild the book

### 0. One-time setup (new computer)

1. Install Quarto from <https://quarto.org/docs/get-started/> (it includes everything needed for the website and the Typst PDF).
2. For the LaTeX PDF (`pchem1.pdf`), install TinyTeX once:
   ```bash
   quarto install tinytex
   ```
3. Any text editor works. VS Code or Positron with the Quarto extension gives a preview button.

### 1. Edit

- Chapters are `01_Basis.qmd` … `15_Kinetics.qmd`; the appendix (thermodynamic data tables) is `A1_Appendix.qmd`; the preface is `index.qmd`.
- The chapter order is the `chapters:` list in `_quarto.yml`.
- New figures go in `img/`. The plots named `img/R_*.png` were drawn once from the R code of the old bookdown chunks (see `_bookdown-archive/`); they can be replaced by new figures at any time.

### 2. Preview while writing

```bash
quarto preview
```

This opens the book in the browser and reloads it every time you save. Stop it with Ctrl+C.

### 3. Build the website and the PDF

```bash
quarto render
```

Everything goes into `docs/` (the website and `docs/pchem1.pdf`). Check for warnings at the end of the output.

### 4. Publish

```bash
git add -A
```

```bash
git commit -m "Describe the change"
```

```bash
git push
```

GitHub Pages serves the `docs/` folder of the `master` branch; the site updates a minute or two after the push.

---

## Writing cheat sheet

| What | How |
|---|---|
| Numbered equation | `$$ E = h\nu $$ {#eq-planck}` |
| Figure | `![Caption.](img/file.png){#fig-name fig-alt="Description for screen readers" width="80%"}` |
| Table | Markdown table, then a line `: Caption. {#tbl-name}` |
| Section label | `## Title {#sec-name}` |
| Reference | `@eq-planck`, `@fig-name`, `@tbl-name`, `@sec-name` (Quarto adds "eq.", "figure", "table", "section", "chapter"). Use `@Fig-name` at the start of a sentence; `[@fig-name]b` for a panel. |
| Unnumbered heading | `## Title {.unnumbered}` |
| Definition / exercise | `::: {#def-name}` … `:::` and `::: {#exr-name}` … `:::`; reference with `@def-name`, `@exr-name` |
| Collapsible answers | `::: {.callout-tip collapse="true" icon="false"}` / `## Answers` / … / `:::` |

Every image needs `fig-alt` (accessibility).

---

## Files

- `_quarto.yml`: book settings (title, chapter list, website theme, PDF layout).
- `quarto.css`, `punctuation.html`, `sidebar-toc.html`: website layout and tweaks (top bar with title, tools, and the group logo in light/dark versions; left sidebar with search and expandable chapter sections; no right-hand column; caption contrast; scrollable equations and wide tables; no line breaks before punctuation after math).
- `mathjax-macros.html`: the `\standardstate` symbol for the website (the PDF defines it in `_quarto.yml`).
- `scripts/sidebar_sections.py`: post-render step that builds the sidebar section lists.
- `_quarto-typst.yml`: optional Typst PDF, `quarto render --profile typst --to typst` (output in `_book-typst/`, not published).
- `_bookdown-archive/`: the former bookdown sources and the conversion script, for reference only.

Old bookdown page names (e.g. `GibbsFree.html`) redirect to the new pages (`09_Gibbs.html`).

---

## License

- **Book text and figures:** [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/), see `LICENSE`. You may share and adapt the book for non-commercial purposes, with attribution, under the same license. Commercial reproduction or resale requires the author's permission. Third-party images (e.g., from Wikipedia) keep their own licenses, as credited in the book.
- **Scripts in `scripts/`:** MIT License, see `scripts/LICENSE`.

This licensing applies from 10 November 2026. Earlier versions of the book remain under the license they were released with (CC BY 4.0 in `LICENSE`; the preface stated CC BY-SA 4.0).
