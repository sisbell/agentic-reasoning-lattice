# Channel Assignment — ASN-0094 review-84

**Date:** 2026-05-25 18:56

## Issue 1: Dead definitions referencing non-foundation ASN
Reason: Dead-text removal is verifiable from ASN-0094's own content — a grep within the document confirms whether `ZeroCountDepth`/`AllocatorTreeDepth` are referenced. The scaffolding clauses already provide the chain-discipline access path the framework actually uses, so no design-intent or implementation question is implicated.

## Issue 2: Defensive paragraph imagines a case the framework already routes
Reason: The fix is internal — EffectiveWpSimplification Step 2's routing on `K ≁ R` vs `K ~ R` (plus per-class constancy's contrapositive `shape(K) ≠ shape(R) ⟹ K ≁ R`) already discharges the case the deleted paragraph imagines. No design-intent or implementation evidence is needed.

## Issue 3: K ∈ T_cat check is implicit in gate ordering
Reason: Editorial restructuring of the gate ordering to surface an explicit `K ∈ T_cat` (and `d ∈ dom(Σ.M)`) gate is derivable from the ASN's own Sh-conf admission conjuncts. No external input required — the fix is a structural rearrangement of already-present content.

## Issue 4: FDD Case B carries a redundant qualifier
Reason: The qualifier's redundancy is fully derivable from FDD's per-class constancy + shape-tuple inequality with R (already established in the FDD section's preamble), which makes "concurrent nullification at FDD-registered K" structurally impossible. Internal cleanup.

## Issue 5: Sh-conf admission "iff" framing conflicts with gate ordering
Reason: Pure logical-form fix — the ASN's own gate ordering and wp_eff form establish that Sh-conf admission is necessary but not sufficient, so restating as a one-direction implication is internal. No external input needed.

## Issue 6: "Three independently-checked structural gates" terminology drifts from the five-gate ordering
Reason: Terminology consolidation between two parts of the same document. The choice of "three structural gates" vs "five-gate ordering" is editorial, derivable from the document's own structure — no design-intent or implementation question informs the choice.

## Issue 7: Lemma — RetractionSelfFreshness preconditions overconstrain
Reason: Restating Precondition 3 so that "Sh4 clause (iii) firing" appears as a consequence of `C = ∅` (which follows from gates 1–4 admitting at K ~ R) rather than a separate commitment is a wording fix derivable from the ASN's own gate ordering and Sh4 contract definition.
