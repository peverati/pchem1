# Bringing the P-Chem 2 website layout to P-Chem 1

**For the Claude session working on P-Chem 1** (`…/_OER_P-Chem_/pchem1`). The author wants the P-Chem 1 website to have *exactly* the same layout as P-Chem 2, live at <https://peverati.github.io/pchem2/>. The reference implementation is in `…/_OER_P-Chem_/pchem2` on `master` (commit `21d893a` or later). Read the files there directly rather than retyping them from this note.

## The target layout

- **Top bar:**
  - book title at the left, linking to the book's home page;
  - GitHub, PDF, and dark-mode buttons at the right;
  - the group logo at the far right, linking to <https://peverati.github.io>;
  - black logo on a white bar in light mode, colored logo on a dark bar in dark mode.
- **Left sidebar:** anchored to the left edge of the window and about 18rem wide. It holds only the search box and the chapter list. Every chapter, and each appendix, has an arrow that expands its sections and subsections; the current chapter starts open and the others start closed.
- **No right-hand column:** the "Table of contents" column is hidden, and the text uses that space, capped at 1050px so lines stay readable.
- **Phones:** two thin bars. The first holds the menu, the three buttons, and the logo at the right. The second holds the chapter-list button, the chapter name, and the search. The page never scrolls horizontally, and long sidebar titles wrap.

## Where P-Chem 1 is now (checked 10 November 2026)

P-Chem 1 already has the *intermediate* P-Chem 2 layout: the logo placed by `logo.html`, `search: true`, the right-hand table of contents, and no top bar. Its `sidebar-toc.html` (the chapter arrows) is current and already includes the MathJax re-typeset for section titles with math (P-Chem 2 has now copied that back), and `scripts/sidebar_sections.py` is identical. Keep P-Chem 1's own `mathjax-macros.html`, the `def-`/`exr-` cross-reference prefixes, and anything else specific to that book.

## Steps

### 1. Files

| Action | File |
|---|---|
| Keep, already up to date | `sidebar-toc.html`, `scripts/sidebar_sections.py`, `punctuation.html`, `img/logo-light.png`, `img/logo-dark.png` |
| **Delete** | `logo.html`, and remove it from `include-after-body` (the top bar now shows the logo natively) |
| **Replace with pchem2's version**, then re-add anything P-Chem 1 had of its own | `quarto.css` |

In `quarto.css`, remove every `.lab-logo` rule, which belonged to the old `logo.html`.

### 2. `_quarto.yml`

Use `pchem2/_quarto.yml` as the model. The layout-relevant parts:

```yaml
project:
  post-render: scripts/sidebar_sections.py   # already there
  resources:
    - .nojekyll
    - img/logo-light.png
    - img/logo-dark.png

book:
  repo-url: https://github.com/peverati/pchem1
  repo-branch: master          # without this, "Edit this page" links point to a non-existent "main"
  repo-actions: [edit, issue]
  downloads: [pdf]
  search:
    location: sidebar
    type: textbox
  navbar:
    logo:
      light:
        path: img/logo-light.png      # each mode needs a {path, alt} object: plain strings fail validation
        alt: "Peverati research group logo"
      dark:
        path: img/logo-dark.png
        alt: "Peverati research group logo"
    logo-href: https://peverati.github.io
    title: false                      # logo-href would also apply to the title, so the title is a separate item
    left:
      - text: "The Live Textbook of Physical Chemistry 1"
        href: index.qmd
  page-footer:
    center: "…license line, see below…"

format:
  html:
    theme:
      light: cosmo
      dark: darkly
    css: quarto.css
    include-after-body:
      - sidebar-toc.html            # logo.html removed
    page-layout: full               # no right-hand column
```

**License footer:** P-Chem 2 uses "Text and figures: CC BY-NC-SA 4.0 · Figure scripts: MIT". P-Chem 1's `LICENSE` file is currently **CC BY 4.0**. Ask the author which license P-Chem 1 should use before writing the footer; don't copy P-Chem 2's footer blindly. If P-Chem 1 switches too, replicate the P-Chem 2 commit `0e1da2f`:

- the official legal code in `LICENSE`;
- `scripts/LICENSE` (MIT);
- the license sentence in the preface;
- a License section in the README, including the date of the change.

### 3. What each CSS block in `quarto.css` does (don't drop any)

- **Caption contrast** (`#595959`, and `#b8b8b8` in dark mode).
- **Wide display equations:** they scroll instead of overflowing. `min-width: 0 !important` is required, because MathJax puts an inline `min-width` on numbered equations, and that alone pushes phone pages wider than the screen.
- **Narrow screens:** `#quarto-sidebar { max-width: 100vw }` plus wrapping titles. Quarto's phone sidebar is otherwise about 430px wide on a 375px screen, which hides the arrows. Also, the breadcrumb in the second bar must be allowed to shrink.
- **Hidden right-hand table of contents:** `#quarto-margin-sidebar nav#TOC { display: none; }`. **Do not** use `toc: false` instead. `scripts/sidebar_sections.py` reads each page's `#TOC` after rendering to build `docs/sidebar-sections.json`, and with `toc: false` the sidebar arrows would have nothing to show.
- **Left-anchored grid (≥992px):** replaces Quarto's centered `page-columns` grid, so the sidebar sits at the left edge with an 18rem column, and `main.content` spans `body-content-start / body-content-end` with `max-width: 1050px`.
- **Top-bar colors:** explicit per mode (`body.quarto-light` → `#ffffff` / `#212529`; `body.quarto-dark` → `#222222` / `#e8e8e8`). `var(--bs-body-bg)` does not work there: in light mode the bar stays dark and the black logo disappears.
- **Logo size and position:** 46px high, moved to the far right with flex `order: 999` on `.navbar-brand-container`. Quarto always puts the brand at the left, and the tools div has `order: 900`, so the brand needs a higher number.

### 4. Build and check

1. Always build with a full `quarto render`. `quarto render --to html` (or `--to pdf`) empties `docs/` first, so the other format's output disappears.
2. Confirm 0 warnings, and that `docs/sidebar-sections.json` and `docs/.nojekyll` exist.
3. Serve `docs/` (for example, `python3 -m http.server --directory docs`) and check:
   - **1920px wide:** sidebar at x≈0, text right after it, no centered empty strip on the left.
   - **1100px:** no horizontal scroll.
   - **375px (phone):** logo at the right of the top bar, chapter arrows visible when the sidebar is open, `scrollWidth == innerWidth`.
   - **Light and dark:** the right logo shows in each, and the bar matches the page background.
   - **Arrows:** expanding another chapter's sections works, and section titles with math render, not as raw `\(…\)`.
   - **Links:** "Edit this page" points to `/edit/master/`.
4. When testing CSS changes in the browser, reload with the cache bypassed. Browsers keep the old `quarto.css` cached, which looks like the change didn't work.

### 5. Known trade-off to mention to the author

Hiding the right-hand table of contents also hides the "Edit this page" and "Report an issue" links on wide screens; they live inside the same box. They still appear at the bottom of each page on phones. P-Chem 2 accepted this.

### 6. Commit and publish

Same rules as for P-Chem 2:

- work on a branch;
- commit only when the author asks;
- push only with the author's explicit approval, because the repository and the site are public;
- after pushing, wait for the GitHub Pages build (`gh api repos/peverati/pchem1/pages/builds/latest`), then spot-check the live site.
