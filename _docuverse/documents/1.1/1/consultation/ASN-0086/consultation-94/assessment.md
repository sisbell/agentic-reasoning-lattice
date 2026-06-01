# Channel Assignment — ASN-0086 review-94

**Date:** 2026-05-31 18:47

## Issue 1: R7a's claim is buried in meta-prose that defends rather than states
Reason: Pure editorial restructuring — restate the formal quantified claim first, relocate the meta-commentary and the clause-(b) non-independence parenthetical (already captured in the dependency list). No design intent or implementation evidence is involved; the fix operates entirely on the ASN's existing text.

## Issue 2: WP Case 2 asserts a weakest precondition (`≡`) but proves only sufficiency
Reason: The necessity direction is derivable from the ASN's own definitions of `nullified`, `Emit_K`, `NoCraftedSpanReachesD`, and the coverage-equivalence membership rule — each dropped conjunct exhibits an `a ∈ nullified(Σ')` witness using machinery already present (R0a, L12a, the regime analysis). No external channel needed.

## Issue 3: The reduction-to-`Emit_K` result is stated twice; supporting prose restates foundation facts and conventions
Reason: Deduplication and trimming of restated foundation facts (L0/SC-NEQ already imported from ASN-0093) — the citations stand on their own and the duplicated reduction/un-nullify prose is internal redundancy. No design-intent or implementation question arises from removing restatements.
