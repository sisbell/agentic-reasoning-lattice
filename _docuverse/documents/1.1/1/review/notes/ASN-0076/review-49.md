# Review of ASN-0076

I worked through every claim (E0–E11), the worked example, and the foundation appeals. The mathematics is sound: the composite is correctly shown to be a ValidComposite★, every K.λ precondition is discharged at each intermediate state with both emission sub-cases covered, boundary cases (first vs. subsequent emission, fresh `ℓ_new` branch vacuity, `#E≥2` preservation under `inc(·,0)`) are handled, the wp in E11 is genuinely non-trivial and correctly pulled back through E10's frame, and the worked example checks the postconditions against concrete tumblers. No cross-ASN references outside the foundation set, no reinvented notation, no out-of-scope claims.

The remaining issues are anti-bloat (this note carries `review-mode.anti-bloat`): interpretive prose that pre-states or restates formal claims.

## REVISE

### Issue 1: E4 "Interpretation" pre-states E7's formal claim
**ASN-0076, E4 Interpretation paragraph**: "By PrefixSpanCoverage, the canonical unit-depth span at `x` has coverage `{t : x ≼ t}`, which contains `x` itself ... The supersession link therefore stands in a permanent structural relationship to the two link entities it relates."
**Problem**: This is exactly E7's content — `ℓ_old ∈ coverage(Σ'.L(ℓ_sup).e₁)` is proved in E7 via "PrefixSpanCoverage and reflexivity," three claims later — and the "permanent structural relationship" assertion previews E9. A precise reader must read the same coverage-membership derivation twice (informally here, formally in E7). The interpretive paragraph advances no reasoning the formal claims do not.
**Required**: Drop the E4 Interpretation paragraph (or reduce it to a single forward pointer to E7), letting E7 carry the coverage statement once.

### Issue 2: Skippable rhetorical section lead-ins
**ASN-0076, lead-ins to E1, E9, E10, E5**: e.g. "The center of the construction is what does not happen." (before E1); "The same argument that protects the original protects the supersession assertion." (before E9); "The transition frame of K.λ tells us what EDITLINK does *not* do." (before E10); "The asymmetry between immutable link entities and mutable supersession assertions reveals a property absent from in-place edit models." (before E5).
**Problem**: These sentences restate, in rhetorical form, what the following proof establishes — they are skippable on the formal chain. (This is distinct from the substantive interpretive remarks in E7-close and E11-collapse, which *do* advance the discoverability distinction and should stay.)
**Required**: Remove the pure-rhetoric lead-ins; keep the codas that introduce new content (the E7→E11 discoverability distinction, the E11 collapse argument).

## OUT_OF_SCOPE

The eight Open Questions (supersession chains/cycles, retraction semantics, successor-designation convention, authorization of `d_new`, multi-link supersession) are correctly deferred — they concern conventions and operations beyond a single link-edit composite.

VERDICT: REVISE
