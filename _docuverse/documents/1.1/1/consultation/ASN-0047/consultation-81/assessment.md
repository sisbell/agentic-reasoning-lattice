# Channel Assignment — ASN-0047 review-81

**Date:** 2026-05-17 16:14

## Issue 1: Cross-document disjointness lemma Case B mixes load-bearing structural lifting with T10a-allocator case enumeration
Reason: Fix is internal — the structural lifting from `d₁ ⋠ d₂ ∧ d₂ ⋠ d₁` to anchor incomparability is self-contained; the (i)/(ii)/(iii) enumeration only needs to be marked motivational, or the lemma rephrased so the enumeration isn't load-bearing. The ASN's own ghost-base treatment already supplies the relevant scope.

## Issue 2: S8 unqualified in ExtendedReachableStateInvariants but qualified in the discharge lemma
Reason: Fix is internal — the S8 discharge lemma in the proof body already specifies the per-subspace decomposition; aligning the invariant list with the lemma is purely a consistency edit.

## Issue 3: Broken forward reference to "Other admissible decompositions"
Reason: Editorial fix derivable from the ASN — either add the missing section or remove the parenthetical reference.

## Issue 4: K.δ ghost-base freshness — cross-allocator distinctness handled implicitly
Reason: Fix is internal — the *Rejection model* paragraph already establishes sequential single-event semantics; adding one sentence at the ghost-base discharge site or deferring concurrent-allocation handling to the existing Open Questions block is sufficient.

## Issue 5: Definition introductions enumerate downstream consumers (meta-prose accretion)
Reason: Editorial cleanup — removing forward-pointing use-site inventories doesn't alter the definitions' content, and downstream sections already cite back when they appeal.

## Issue 6: Document-ordering justification prose
Reason: Editorial trim — the deferral pointer is self-explanatory; meta-commentary about why the order works is removable without loss.

## Issue 7: SubAllocatorAxiom — axiom prose explains why rather than what
Reason: Editorial compression — the axiom clauses (Exists, Disjoint, Namespace) are self-contained; the multi-paragraph reconciliation rationale can be condensed to one sentence without changing the axiom's content or its discharge dispatch.

## Issue 8: Worked example notation switching adds reading overhead
Reason: Editorial cleanup — the section preamble already partly handles the four-component reduction; consolidating it once and dropping per-line annotations is a presentation choice fully derivable from the example's own structure.
