# Review of ASN-0047

This ASN is exceptionally thorough — the structural Class (a) / Class (b) distinction by temporal scope, the explicit dependency chain for K.μ~ (Steps A → E), the detailed verification matrix with per-(invariant, transition) discharge, the six worked examples (entity hierarchy by K.δ, fork with subsequent insertion, interior content replacement, link allocation + arrangement, etc.), and the careful handling of edge cases (empty arrangements, singleton dom_C, full-clearance vs partial-suffix K.μ~ realisations, prefix-comparable vs prefix-incomparable cross-document discharge) all demonstrate Dijkstra-grade rigor. The treatment of subspace preservation as a *derived* consequence rather than a prerequisite of S3★(Σ') correctly avoids circularity. The proof that pointwise link-subspace fixity follows from CL-UNIQ but post-state CL-UNIQ preservation does *not* require Step (4) is a careful distinction that lesser specifications would conflate.

The items below are presentational refinements.

## REVISE

### Issue 1: Empty endset semantics deferred from Open Questions

**ASN-0047, "Semantics of empty endsets at slots 1 and 2"**: "Whether to narrow K.λ with a stricter `e₁ ∪ e₂ ≠ ∅` precondition is recorded as *design-uncertain* and left to a future operations ASN" appears in the body but is not listed in Open Questions.

**Problem**: In-body design-uncertain items may escape the visibility scan that downstream ASN authors and reviewers run against Open Questions. Nelson's "one-sided link" case (LM 4/48) and the type-only marker case are both admitted by L3 but have distinct semantic interpretations the ASN doesn't formally distinguish.

**Required**: Add to Open Questions: "Should K.λ require `e₁ ∪ e₂ ≠ ∅` to exclude type-only links, or admit them as valid markers per Nelson's one-sided link case (LM 4/48)? If admitted, do one-sided links (exactly one of e₁, e₂ empty) and type-only markers (both empty) carry distinguishable semantics in endset-iterating consumers like L8's `same_type` and the discovery-set unions?"

### Issue 2: Inconsistent labeling of K.μ~ full-clearance convention in verification matrix

**ASN-0047, Class (a) verification matrix**: Most K.μ~ cells explicitly label "K.μ⁻ (full-clearance)" (S2, S3★-aux, S8a/S8-depth/S8-fin, D-CTG★/D-MIN★), but the S3★ cell ("K.μ⁻ restriction + K.μ⁺ amendment alone"), the S8★ cell ("link-subspace via fixity... content-subspace decomposition rebuilt..."), and the D-SEQ★ cell ("derived at Σ' from the K.μ~-chain post-state values...") omit this tag.

**Problem**: The matrix-preamble note states that K.μ~ matrix entries invoke the full-clearance form by default, but inconsistent tagging across the rows may obscure the discharge route for readers cross-referencing specific cells against the K.μ~ Decomposition section. The full-clearance convention is load-bearing for cells whose K.μ⁻ step needs the strongest possible (n'_{s_C} = 0) admissibility guarantee.

**Required**: Uniformly tag every K.μ~ matrix cell with "(full-clearance)" where the convention applies — at minimum the S3★, S8★, and D-SEQ★ rows — so the discharge route is visible at every cell rather than implicit through the preamble note.

VERDICT: REVISE
