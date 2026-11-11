# Style checklist (P-Chem 1, new edition)

Reference style (from P-Chem 1 at its best and from P-Chem 2): colloquial "we", guiding the reader step by step, analogies (the stick, the machine and its knobs, NYC–LA, the coins), every derivation step explained in words, rigorous concepts even when that means dropping a misleading convention, little math assumed.

Items marked **(rigor)** state something imprecise or wrong. The others are places where the text stops guiding the reader.

## Book-wide
- [ ] Most chapters start straight with a section, without the short opening that links to the previous chapter and says what this one does (as in P-Chem 2). Only ch. 5, 6, 7, 9 and 14 have one.
- [ ] Key results are rarely followed by an interpretation ("A few important considerations…" list), as P-Chem 2 does.
- [x] Practice problems removed from every chapter (11 November 2026; they will move to a separate problem website). Study questions rewritten: 10 per chapter on the key concepts, 5 options each.

## Chapter by chapter
- **Preface:** OK. The author's note is dated 2024 and needs a new-edition update.
- **1 Introduction:** voice OK. **(rigor)** The "Infinite Slicing" passage says differentials are "unitless but not dimensionless" and are "0.000[…]0001 m". Both are misleading, since dL has units of length.
- **2 Zeroth Law:**
  - [ ] The opening defines heat and work through "external/internal parameters" without explaining what those are.
  - [ ] The zeroth law section starts from "equivalence relation" jargon. It needs an intuitive lead-in, or the order swapped with the coin example.
  - [ ] **(rigor)** The work derivation uses P where it should be P_ext (the two only coincide for reversible processes), and the difference is never stated.
- **3 First Law:**
  - [ ] **(rigor)** "Work becomes a state function" (adiabatic) and "heat becomes a state function" (isochoric) are misleading. Q and W equal ΔU in those cases; they don't change nature.
  - [ ] **(rigor)** The Joule experiment says the water bath is "to guarantee isolation" and gives the wrong reason for P_ext = 0.
  - [ ] The definition of a reversible process is a terse quote from Sears; it needs our own explanation.
- **4 Thermochemistry:** voice OK. **(rigor)** The opening says reactions absorb or release "the energy contained in these bonds". That is the classic misconception: breaking bonds always costs energy.
- **5 Thermodynamic Cycles:** voice OK.
  - [ ] **(rigor)** The history says Carnot's "experiments" settled the Joule–Kelvin controversy.
  - [ ] The Carnot stage images are text-heavy Wikipedia panels.
  - [ ] "Energy, Heat, and Work in the Carnot Cycle" is a chain of equations with almost no words.
- **6 Second Law:** ✅ rewritten on 11 November 2026 (entropy defined as dS = đQ_rev/T with interpretation list, guided Carnot algebra, second-law derivation with plausibility note, Boltzmann section rewritten around a 4-molecule counting example that reproduces nR ln 2, new practice problem 3).
- **7 Third Law:** OK. Minor: the claim that "the surroundings always absorb heat reversibly" is hand-wavy.
- **8 Thermodynamic Potentials:** least guided chapter after ch. 13.
  - [ ] Legendre transformations, conjugate variables (dense footnote) and Maxwell relations come with no plausibility explanation or intuition for weak-math students.
  - [ ] "The thermodynamic potentials are the analog of the potential energy…" is now left hanging; it needs the interpretation that sentence promises.
- **9 Gibbs Energy:**
  - [ ] **(rigor)** The "Composition dependence" integration ("G = 0 when n = 0", integrating μ* dn) is hand-wavy.
  - [ ] **(rigor)** The entropy criterion counts moles of everything; it should count moles of gas.
- **10 Chemical Equilibrium:** mostly OK. The activity paragraph (ideal gas, real gas, pure solids, solutions, all at once) is a dense list.
- **11 Ideal and Non-Ideal Gases:**
  - [ ] **(rigor)** The fugacity section's step "since μ = μ° when P = P°, it is easy to demonstrate that f/P → 1" is a non-sequitur.
  - [ ] The compressibility-factor derivative "near P = 0" skips all steps.
- **12 Phase Equilibrium:**
  - [ ] **(rigor)** The solid's μ line is called "flat because the entropy of a solid is about zero by the third law"; that only holds near 0 K.
  - [ ] **(rigor)** The skating footnote repeats the pressure-melting explanation, a known misconception: friction heating and the surface layer of the ice dominate.
- **13 Multi-Component Phase Diagrams and Solutions:** ✅ rewritten on 11 November 2026 (opening, ideal-solution definition, guided diagrams, Henry's law, activity and colligative derivations, 4 practice problems). Still open: the hand-drawn figures, two of which say "Roult's Law"; redraw them in the book-wide figure pass.
- **14 Chemical Kinetics:**
  - [ ] **(rigor)** "First-order … therefore also called unimolecular" mixes up order and molecularity, which the chapter itself separates later.
  - [ ] **(rigor)** "A and Ea are always positive, no known exception" overstates; negative apparent activation energies exist.
  - [ ] The consecutive-reactions discussion (k₁ ≅ k₂ described as a "rate-determining step in the middle") and the steady-state approximation are confusing.
- **Appendix:** data tables, OK.
