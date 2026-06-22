Reading through the foundation statements and the five claims in ASN-0053.

**S0** carries out its ≤-compositions by explicit four-case unfolding and is correct. Its formal contract even documents the omission: "The non-strict compositions the proof needs … are *not* T1 exports; each is derived in the proof by case analysis on the abbreviation." S2 trivially delegates to T12(b) and is sound. S6 applies TumblerAdd's result-length identity directly under the stated preconditions and is correct. Both WF and S11 contain proof gaps that cross the soundness threshold.

---

### WF: mixed `<`+`≤` chain cited as strict transitivity
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder)
**ASN**: WF (WellFormedSpanFromEndpoints) — "it would force #s + 1 ≤ #s, which set against NAT-addcompat's strict successor inequality #s < #s + 1 produces the chain #s < #s + 1 ≤ #s, hence #s < #s by NAT-order's transitivity"
**Issue**: NAT-order's transitivity axiom is `(A m, n, p ∈ ℕ : m < n ∧ n < p : m < p)` — strictly `<`+`<` → `<`. NAT-order's named consequence ≤-transitivity is `≤`+`≤` → `≤`. Neither rule covers the mixed chain `#s < #s+1 ≤ #s → #s < #s` that the proof needs. The `≤` in the middle requires prior case analysis: `#s+1 ≤ #s` unfolds to `#s+1 < #s ∨ #s+1 = #s`. In the first sub-case, strict transitivity with `#s < #s+1` yields `#s < #s`. In the second sub-case, substituting `#s+1 = #s` into `#s < #s+1` yields `#s < #s`. The proof skips both sub-cases and instead names a rule that does not apply to the mixed chain.
**What needs resolving**: The T1 case (ii) elimination must case-split on the definition of `≤` — unfolding `#s+1 ≤ #s` into `#s+1 < #s` and `#s+1 = #s` — and derive `#s < #s` separately in each sub-case before invoking NAT-order's irreflexivity.

---

### S11 tightness: `start(α) ≤ t` asserted, not derived, before invoking S0
**Class**: REVISE
**Foundation**: T1 (LexicographicOrder)
**ASN**: S11 (DifferenceBound) — "start(α) < start(β) ≤ t < reach(β) places t between two members of ⟦γ⟧. By S0 (convexity), t ∈ ⟦γ⟧"
**Issue**: S0's precondition is `p ≤ q ≤ r` with p = start(α), q = t, r = reach(β). The proof needs `start(α) ≤ t`. The available chain is `start(α) < start(β) ≤ t`, a mixed `<`+`≤` composition. T1 does not export ≤-transitivity — S0's own formal contract states this explicitly ("are *not* T1 exports; each is derived in the proof by case analysis on the abbreviation"). The step `start(α) ≤ t` from `start(α) < start(β) ≤ t` requires case-splitting on `start(β) ≤ t` (i.e., `start(β) < t ∨ start(β) = t`) and applying T1(c) or substitution in each sub-case to obtain `start(α) < t`, then weakening to `≤`. The proof asserts the result without carrying out the case analysis that the system's own design mandates.
**What needs resolving**: The tightness sub-argument must derive `start(α) ≤ t` explicitly by case-splitting on `start(β) ≤ t` before invoking S0, mirroring the technique S0 itself uses to compose ≤-steps.

---

VERDICT: REVISE