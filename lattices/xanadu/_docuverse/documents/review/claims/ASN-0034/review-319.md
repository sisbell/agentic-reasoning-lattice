# Cone Review — ASN-0034/D2 (cycle 6)

*2026-04-18 19:18*

### TumblerSub's precondition-consequence case (ii) omits the Divergence sub-case (ii-a) / (ii-b) enumeration that D0, D1, and D2 perform explicitly

**Foundation**: Divergence's Definition splits case (ii) into sub-case (ii-a) (`#a < #b` with `divergence(a, b) = #a + 1`) and sub-case (ii-b) (`#b < #a` with `divergence(a, b) = #b + 1`), selected by NAT-order's trichotomy at the length pair. D0, D1, and D2 each enumerate both sub-cases by label when eliminating Divergence case (ii), and their Depends entries itemise the sub-case-specific elimination mechanisms (D0's sub-case (ii-a) via NAT-addcompat/NAT-order, sub-case (ii-b) via T1; D1 and D2 similarly).

**ASN**: TumblerSub's precondition-consequence proof — "Two Divergence cases arise for the pair `(w, a)` with `w ≠ a`: … (ii) Prefix divergence — `w` is a proper prefix of `a` (the direction forced by `w < a` via T1 case (ii)), so `#w < #a` and `wᵢ = aᵢ` for all `1 ≤ i ≤ #w`. The padded extension sets `wₖ = 0` for `k > #w`…"

**Issue**: Divergence case (ii) applied to pair `(w, a)` has two sub-cases: (ii-a) `#w < #a` with `divergence(w, a) = #w + 1`, and (ii-b) `#a < #w` with `divergence(w, a) = #a + 1`. TumblerSub's narrative leaps to sub-case (ii-a)'s conclusion (`w` is a proper prefix of `a`, `#w < #a`) without naming either sub-case or explicitly excluding sub-case (ii-b). The "direction forced by `w < a` via T1 case (ii)" parenthetical gestures at the exclusion but does not spell it out: sub-case (ii-b) would make `a` a proper prefix of `w`, yielding `a < w` via T1 case (ii) and contradicting the derived `w < a` — the same mechanism D0's sub-case (ii-b) elimination uses. TumblerSub's Divergence Depends entry reads only "the precondition consequence proceeds by case analysis on Divergence's two cases for the pair `(w, a)`", without itemising which sub-case the analysis lands in or how the other is ruled out.

**What needs resolving**: Either rewrite TumblerSub's case (ii) to enumerate sub-cases (ii-a) and (ii-b) and eliminate the latter via T1 direction (matching D0's pattern), or justify in the prose and Depends why the consolidated "w is a proper prefix of a" phrasing is sufficient at this site despite the sub-case-explicit convention D0/D1/D2 follow for the same Divergence case.
