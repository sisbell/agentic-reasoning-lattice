# Channel Assignment — ASN-0043 review-171

**Date:** 2026-05-31 02:51

## Issue 1: The `Σ' ⊒ Σ` (StateExtension) discharge is duplicated verbatim across L9 and L11b
Reason: Purely structural deduplication — FSP already holds all three StateExtension conjuncts (h1 freshness, the C/M equalities), so adding `Σ' ⊒ Σ` to its conclusion and citing it at both call sites is derivable from the ASN's own proof content. No design intent or implementation evidence is at stake.

## Issue 2: L8 "Consequences" expands a trivial inheritance into three formula-bullets that do no work
Reason: Pure editorial condensation of `same_type` inheriting reflexivity/symmetry/transitivity from set equality; the reasoning is already fully present in the ASN and needs no external input.
