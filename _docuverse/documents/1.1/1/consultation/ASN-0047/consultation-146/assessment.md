# Channel Assignment — ASN-0047 review-146

**Date:** 2026-05-31 15:05

## Issue 1: LinkVPositionDepthAxiom fixes `m_L = 2` by axiom on implementation evidence alone
Reason: The fix can take two forms — abstract the axiom to "fixed `m_L ≥ 2` per document" (internal) or ground the specific value `2` in design intent rather than `do2.c`. Determining whether `2` is genuinely forced (vs. an incidental implementation choice) requires Nelson's design intent; the abstraction fallback is otherwise derivable.
Nelson question: Is the link-subspace V-position depth intended to be a specific fixed value (and in particular to match the content-subspace V-position depth), or is the design satisfied by any fixed per-document link depth?

## Issue 2: Axiom prose inventories downstream use-sites and explains why-needed rather than stating the axiom
Reason: Purely editorial — reducing NodeUniqueAllocation/NodeRegistryBootstrap to their conditions and relocating use-site pointers is derivable from the ASN's own structure.

## Issue 3: Document-ordering justification prose in the state model
Reason: Deleting the presentation-order justification requires no external input; the `L = ∅` reading follows from `L₀ = ∅`, already stated.

## Issue 4: K.μ~ dependency-chain prose argues non-circularity repeatedly
Reason: Removing standalone non-circularity assertions is internal; each step's premises are already listed and the dependency is visible from them.

## Issue 5: Triple statement of the "K.α has no local amendment" point
Reason: Consolidating the three restatements into one home with a pointer is purely editorial and derivable from the ASN.

## Issue 6: K.δ k=1 provenance case-split and "operational uniformity" explained redundantly
Reason: Deduplicating the (a')/(b') dispatch, folding the uniformity remark, and relocating the multi-version elaboration are internal reorganisations; the content already exists in the ASN.

## Issue 7: FrontierEquivalence "Significance" and "Counterexample" meta-prose
Reason: Deleting "Significance" and reducing the counterexample is internal — whether any carrier relies on the T4b-non-identification fact is checkable within the ASN itself.
