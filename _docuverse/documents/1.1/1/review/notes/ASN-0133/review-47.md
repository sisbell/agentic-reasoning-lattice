# Review of ASN-0133

The logic is sound. I worked through Q0's view-rebuild (the four view-parameterized atoms, the four UV-rewritten behavior collections, and the view-stable remainder are each accounted for, and `chain` correctly routes through `elems`), the Q1/Q5/Q5a counting injections, Q-EXT as the X-DEF+PD0 composition, the H-SFAIR ⟹ H-FAIR implication (both the infinitely- and finitely-recurring branches), the regime-form derivation, and Q6's three obstructions with the H-SFAIR closure of case (3) — all hold. The worked composition (audit-spelling SF triggers, extinction via the Marker pattern, the Q5a domain bound, the reached-terminal-state trace) checks out against the cited foundations, and foundation usage is consistent (no reinvented notation, no non-foundation cross-refs). Findings are anti-bloat / precision only.

## REVISE

### Issue 1: Regime (ii)'s grow-only argument is re-derived inside obstruction (3)
**ASN-0133, Q6 proof (obstruction 3 discussion)**: "impossible where domains are grow-only (there removal is barred, so weak H-FAIR collapses to firing-or-in-place-falsification, each of the finitely many arguments is eventually settled, and quiescence is reached *and* held — the clean grow-only contrast of regime (ii))"
**Problem**: This near-verbatim restates the grow-only result established a few sentences earlier in regime (ii) ("a grow-only domain cannot shrink, so H-FAIR's removal escape is unavailable… each of the finitely many arguments is thus eventually settled… so quiescence is reached and held"). The parenthetical even self-labels itself "the clean grow-only contrast of regime (ii)" — naming the passage it duplicates. This is exactly the "two paragraphs say the same thing in different words" pattern the anti-bloat classifier targets.
**Required**: Replace the re-derivation with the back-reference it already gestures at — e.g. "…impossible where domains are grow-only (regime (ii): removal barred)." The contrast survives; the duplicated mechanism goes.

### Issue 2: "strong-scheduling form of regime (i)" framing is undercut by the satisfiability caveat it follows
**ASN-0133, H-SFAIR, *Satisfiability is environment-conditional***: "that is just regime (i)'s per-rule cooperation secured by scheduling rather than supplied by the environment directly: H-SFAIR is the *strong-scheduling form* of regime (i), not a disjoint second route."
**Problem**: Two sentences earlier the paragraph states the regime form is "satisfiable only under a turn-fairness in which the scheduler eventually fires any recurrently-*presented* argument," and its own add-remove counterexample shows a scheduler *cannot* fire an argument the environment withdraws before every turn. So the turn-fairness H-SFAIR requires is a *joint* scheduler+environment condition — the environment must leave recurrently-presented arguments present at some turn — not something "secured by scheduling rather than supplied by the environment." The framing asserts a scheduling-vs-environment dichotomy the paragraph's own counterexample undercuts, and "not a disjoint second route" is editorial categorization that does no work downstream (Q6's formal content rests on the regime form, not on this identification). Compounding it, H-SFAIR + bounded growth reaches-and-holds even when the environment never idles (e.g. endless content deposits), so it is strictly more general than regime (i) as a condition, not a sub-form of it.
**Required**: Drop the "strong-scheduling form of regime (i)" sentence, or restate it to say H-SFAIR is a distinct sufficient condition for reach-and-hold — overlapping regime (i) in outcome, requiring environment turn-fairness as well as scheduler aggression — rather than a sub-form secured by scheduling alone.

## OUT_OF_SCOPE

The five open questions (the `pd_extinct` SF certificate, a runtime divergence detector, per-scope vs global work, cross-scope oscillation, contract necessity) and the four "What this note doesn't cover" deferrals (scheduler, stochastic bodies, activation binding, environment model) are correctly scoped as future/implementation-layer work; none is an error in this note.

VERDICT: REVISE
