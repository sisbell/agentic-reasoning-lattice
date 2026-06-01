# Channel Assignment — ASN-0047 review-178

**Date:** 2026-05-31 22:26

## Issue 1: Foundation typing override asserted but not demonstrated to transfer
Reason: The fix is internal — the transfer obligation is a formal derivation over the ASN's own inherited results, requiring either enumeration of each `dom(M)`-phrased foundation result under the `dom(M) ⟺ E_doc` substitution or explicit confinement of the override's scope. Neither design intent nor implementation evidence bears on the soundness of a notational substitution.

## Issue 2: Logical direction of the `e ∉ E` discharge is backwards / circular
Reason: The fix is internal — disentangling caller-checked precondition from allocator-discipline consequence is pure proof-structure repair derivable from the ASN's own definitions of GlobalUniqueness, FrontierEquivalence, and `inc` determinism.

## Issue 3: SubAllocatorAxiom prose explains clause provenance instead of advancing the axiom
Reason: The fix is internal and editorial — state the five clauses directly and inline-label Disjointness as a local lemma, deleting the inherited-vs-local meta-paragraph; no external evidence is implicated.

## Issue 4: K.δ k=0 discharge is restated near-verbatim across three sections
Reason: The fix is internal and editorial — consolidate the abstract k=0 discharge into one location with named cross-references, a structural deduplication requiring no design or implementation input.

## Issue 5: Presentation-justification prose in the K.μ~ precondition argument
Reason: The fix is internal and editorial — delete the single meta-sentence justifying the separation of the necessity/sufficiency directions; no external channel is involved.
