# Handoff: revising the P-Chem 1 textbook using P-Chem 2 as the model

This file summarizes the November 2026 revision of *The Live Textbook of Physical Chemistry 2* (project in `…/_OER_P-Chem_/pchem2`; revised in bookdown, then converted to Quarto on `master`; the bookdown version is on the `bookdown` branch). Use the P-Chem 2 book as the reference for structure, format, and style when restructuring P-Chem 1.

---

## 0. FIRST STEP: convert P-Chem 1 from bookdown to Quarto

P-Chem 2 was moved to Quarto on 10 November 2026 (live at https://peverati.github.io/pchem2/). Do the same for P-Chem 1 **before** any content revision, so that all later edits happen directly in the `.qmd` files. Follow the P-Chem 2 repo as the template:

1. **Keep the bookdown version safe:** create a `bookdown` branch from `master`, then work on a new branch (e.g., `quarto-trial`).
2. **Convert:** adapt `pchem2/_bookdown-archive/convert_to_quarto.py` (change the `CHAPTERS` list and paths). It handles:
   - cross-references (`\@ref(eq:x)` → `@eq-x`, `fig-`, `tbl-`, `sec-`; drops the preceding word; `[@fig-x]b` for panels);
   - equations with `(\#eq:x)` → `$$…$$ {#eq-x}`;
   - figure chunks → Markdown images with `fig-alt`;
   - `knitr::kable` tables → plain Markdown tables (evaluated once with R, so the final book needs no R);
   - `<details>` answer blocks → collapsible callouts; examples → `exm-` blocks;
   - old LaTeX (`{\bf}`, `{\cal}`, `vmatrix`, `$\\$` spacing lines).

   Check its warnings and grep the output for any leftover `\@ref(` or R chunks. P-Chem 1 may have chunk types that P-Chem 2 did not (e.g., other R code, other block types).
3. **Copy the config and website files from pchem2 and adapt them:**
   - `_quarto.yml`: title, chapter list, `repo-url`, `output-file`; keeps `output-dir: docs`, `.nojekyll` and the logos as resources, light/dark themes, LaTeX PDF settings;
   - `_quarto-typst.yml`;
   - `quarto.css`, `punctuation.html`, `logo.html`, `img/logo-light.png`, `img/logo-dark.png`.
4. **Keep the old URLs:** add `aliases: [OldName.html]` front matter to each chapter, using the bookdown chapter IDs (the `{#ID}` of each `#` heading).
5. **Archive** the `.Rmd` files, the bookdown config, the `.Rproj`, and the converter into `_bookdown-archive/`. Delete the old `docs/` and `quarto render` into it.
6. **Check:**
   - `quarto render` reports 0 warnings;
   - no `??` in the HTML;
   - equations, figures, and the PDF link work;
   - light and dark modes both show the right logo;
   - at phone width there is no horizontal page scroll.
7. **Write a README** with the update procedure (copy pchem2's `README.md`). Commit, merge into `master`, and push only after explicit approval.

Known limitations to keep in mind:

- **PDF/UA:** tagged PDF does not work with Quarto's Typst book template yet.
- **LaTeX PDF:** under KOMA `scrbook`, it needs the `\DeclareOldFontCommand` lines that are already in pchem2's `_quarto.yml`.

## 1. Process we followed (in order)

1. **Restructure first.** We swapped chapters, renamed files, and fixed the chapter list in `_bookdown.yml`. Then we built in a scratch copy to confirm that every cross-reference still resolved.
2. **Proofread every chapter** for errors and typos, with fixes applied directly.
3. **Assessment without edits:** what is strong, what is missing, and what is inconsistent.
4. **A prioritized checklist** (`REVISION_CHECKLIST.md`) in tiers:
   1. inconsistencies;
   2. practice;
   3. syllabus gaps;
   4. polish;
   5. interactive content.
5. **Chapter-by-chapter upgrades.** Each followed the same pattern: propose the changes and agree on scope, then write the text, generate the figures, add review questions, and do a test build.
6. **Book-wide passes:**
   - notation consistency;
   - rewriting borrowed passages in the author's voice;
   - replacing all Wikipedia images with computed figures;
   - accessibility (Section 508 / WCAG 2.1 AA);
   - removing misconception-prone language.
7. **Course schedule** (`COURSE_SCHEDULE.md`), sized by each chapter's length and weight.
8. **Commit** on a branch, then a fast-forward merge into `master`. Nothing was pushed without explicit approval.

## 2. Structure and format conventions to replicate

**Chapter anatomy** (the model is chapters 4 and 5 of P-Chem 2):
- **Opening:** a short introduction that links to the previous chapter and says what this one does.
- **Body:** sections built in small steps, with numbered, labeled equations.
- **Interpretation:** after every key result or figure, a numbered list introduced by "A few important considerations can be made by analyzing…", with a **bold lead phrase** per item.
- **Figures:** multiple representations of the same result (equation, plot, map, diagram).
- **Worked numbers in the text:** real molecules and real data (for example, CO's bond length from B, and photon energies in kJ/mol).
- **Ending:** `## Chapter Review {#revN}` / `### Study Questions {#questN}`, with 10–16 conceptual multiple-choice questions. Every question must be answerable from that chapter's text.
- **Answer reveal:** the R inline block. In HTML it outputs `<details><summary>Answers (select to reveal)</summary>…</details>`; in the PDF it outputs plain text.

**Voice and pedagogy:**
- **Voice:** first-person plural ("we"), direct and friendly, aimed at chemistry students who are not strong in math and physics.
- **Math:** explain every derivation step in words, and say when an argument is a plausibility argument rather than a proof.
- **Chemistry first:** tie physics to chemistry (why chemists care), and link forward and backward between chapters with `\@ref()`.
- **Orbitals are not boxes.** Never say electrons are "placed in", "put in", "filling", "going into" or "sitting in" orbitals. Write "described by" an orbital. "Occupied/unoccupied orbital" is defined once as bookkeeping language.
- **No Dirac notation** (bra–ket). Slater determinants are written |χ₁ χ₂ ⋯|. The postulates-as-axioms framing was removed as antiquated.
- **Interpretation:** the book uses Copenhagen language, but says explicitly that it is incomplete (many worlds, Bohmian mechanics, hidden variables, spontaneous collapse).

**Notation and units:**
- Spin functions are α/β. Gravity is `g`. Ångström is written `\text{Å}`.
- Use m_ℓ (never a bare m) for the quantum number.
- Give energies in kJ/mol together with the natural unit (E_h, eV, cm⁻¹), and state the conversions once.

**Figures** (each chapter has its own script in `scripts/make_figures_*.py`, run from the project root as `python3 scripts/<script>.py img`):
- **Style:** matplotlib with `font.family=serif` and `mathtext.fontset=cm`, font size around 16; the default tab color cycle; purple for nodes, special points and annotations; red/blue for positive/negative (or spin up/down).
- **Computed, not hand-drawn:** figures come from real calculations or real data wherever possible. Captions say when a figure is schematic.
- **Every figure chunk has:** a label `figNcM` (number, then chapter), a full `fig.cap`, and a plain-language `fig.alt` (no LaTeX). Example: `` ```{r Fig1c7, out.width='90%', fig.show='hold', echo=FALSE, fig.align='center', fig.cap='…', fig.alt='…'} ``
- **No double quotes in `fig.cap`:** they break the HTML alt attribute.
- **No `\@ref()` inside `fig.cap`:** it doesn't resolve in HTML. Use "the previous figure" instead.
- **No Wikipedia images.** Credit any external source in a footnote.

**Tables:** `knitr::kable(..., escape = FALSE, caption = …)` in an R chunk labeled `tabNcM`.

## 3. Technical setup and gotchas

- **`_bookdown.yml`:** the key must be lowercase `rmd_files`. With `Rmd_files` bookdown ignores the list and builds every .Rmd alphabetically.
- **Renaming chapters:** use `git mv`, renumber figure, table and `{#revN}` labels to match, and check for collisions.
- **Builds:** never build into the author's `docs/`. Copy the source to a scratch folder (`rsync … --exclude docs --exclude .git`) and run `bookdown::render_book("index.Rmd", "bookdown::gitbook")` and `"bookdown::pdf_book"`. Then grep the HTML for `@ref(`, `??` and `&lt;img`, which signal unresolved references or broken images.
- **LaTeX:** TinyTeX lives in `~/Library/TinyTeX` (TeX Live 2026, repository `tlnet.yihui.org`). Run `export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"` first. pdflatex needs no raw Unicode π or σ in headings; write `$\pi$` instead.
- **Accessibility:**
  - `lang: en` in the `index.Rmd` YAML;
  - descriptive link text (never "here");
  - caption color `#595959`;
  - answers inside `<details>`;
  - wide display equations made horizontally scrollable via CSS in `style.css`;
  - a small script in `mathjax-chem.html` that keeps punctuation on the same line as inline math.

  The PDF is not tagged, which is a known limitation.
- **Long equations:** split them with `aligned`, so they don't get cut off on phones.
- **Previewing:** to check HTML behavior, serve the scratch `docs` with `python3 -m http.server` through the browser preview. Check at phone width (375 px).

## 4. Collaboration preferences observed

- **Before large changes:** propose what to change or add as a prioritized list, wait for the go-ahead, then implement everything agreed.
- **Scope:** keep additions lecture-sized ("quick"). The author plans a companion website for practice problems, so the book doesn't need end-of-chapter numerical problems.
- **Data:** flag experimental values written from memory so the author can check them, and mention what couldn't be verified.
- **Git:** commit only when asked; branch first; never push without explicit approval (the repository and website are public).
- **Teaching load:** chapters were originally designed for three classes in one week. After the revision some chapters need more, and `COURSE_SCHEDULE.md` sizes them (15 weeks, MWF, three midterms, 42 lecture slots).

## 5. What the P-Chem 2 revision produced (for reference)

- **Chapters (13):**
  1. Classical physics (Hamiltonian, waves)
  2. Failure of classical physics (black body, photoelectric effect, Bohr model, de Broglie)
  3. Schrödinger equation (wave packets)
  4. Solvable models (box, 3D box, ring, sphere, harmonic oscillator)
  5. Hydrogen
  6. Operators (time evolution)
  7. Spin
  8. Quantum weirdness (measurement, interpretations, double slit, uncertainty, tunneling)
  9. Many-electron atoms (term symbols)
  10. Molecules (Born–Oppenheimer, PES, Hartree–Fock)
  11. Diatomic bonds (H₂⁺, H₂, CI, second-row and heteronuclear diatomics)
  12. Polyatomics (water, Koopmans, localized orbitals, Hückel)
  13. Spectroscopy (selection rules, rotational, vibrational including polyatomics, electronic, Jablonski, NMR/ESR)
- **Figures:** more than 70 computed figures, every one with alt text.
- **Planning files:** `REVISION_CHECKLIST.md` and `COURSE_SCHEDULE.md` sit in the project root and are not part of the build.
