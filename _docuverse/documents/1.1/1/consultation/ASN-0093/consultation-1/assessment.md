# Channel Assignment — ASN-0093 review-1

**Date:** 2026-05-18 13:24

## Issue 1: Missing ContentStoreFiniteness invariant
Reason: Pure structural symmetry with L-fin — the discharge pattern is identical and derivable from `Σ₀.C = ∅` plus K.α's singleton extension. No external evidence needed.

## Issue 2: Forward references to non-foundation ASNs
Reason: Style/self-containment fix internal to the ASN. The substrate's own scope statement already articulates the layering; rewording references to "higher-layer transition models" is an authorial decision.

## Issue 3: C1c chain exhibition imprecise
Reason: Derivable from the substrate's own definitions of `b_C(d)`, `b_L(d)`, and the TA5 inc-step rules in ASN-0034. The content chain has shape `(d, b_C(d), a)` directly from the anchor definitions.

## Issue 4: K.α / K.λ forward-allocation clause asymmetry
Reason: The substrate's own subsequent-emit rule `inc(prev, 0)` makes the clause derivable via T9 (ASN-0034, TA5(a) strict-monotonicity); symmetric removal or symmetric inclusion is an internal authorial choice.

## Issue 5: Missing concrete worked example
Reason: Mechanical instantiation of the substrate's own definitions on chosen tumbler values. No external input required.

## Issue 6: Cross-document disjointness lemma name suggests unused derivation
Reason: Renaming question — the proof body's cited foundations (T10, Prefix, M0, T4) are visible in the text. The author can either rename to match or add the T10a.{2,5} intermediate step from ASN-0034's definitions.

## Issue 7: M0 source citation imprecise
Reason: Pure wording fix in the Properties Introduced table. The discharge matrix already states the correct discipline.

## Issue 8: SubAllocatorAxiom.T10aConformance — bootstrap asymmetry
Reason: The embedding choice (sub-allocators inside T10a's global tree vs. as free-floating T10a-conforming chains) requires understanding whether Nelson's design treats sub-allocators as a unified allocator hierarchy, and whether udanax-green's allocator implementation embeds content/link sub-allocators in a single tree.
Nelson question: Are content and link sub-allocators under each document part of a single global allocator tree rooted at the universal allocator, or do they stand as independent allocator chains per document?
Gregory question: In udanax-green, does the allocator structure embed content and link sub-allocators under each document into the global allocator hierarchy with parent pointers, or are they tracked as independent free-floating chains?

## Issue 9: K.α/K.λ parameter semantics
Reason: Operational clarity convention internal to the ASN's transition-model presentation. The deterministic pinning is already stated; the author chooses whether to present `a`/`ℓ` as input or output.
