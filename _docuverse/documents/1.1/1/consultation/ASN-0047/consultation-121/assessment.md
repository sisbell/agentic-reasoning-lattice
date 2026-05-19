# Channel Assignment — ASN-0047 review-121

**Date:** 2026-05-19 16:37

## Issue 1: Sub-allocator A_v(d) case-split incomplete for K.δ k=0 minted documents
Reason: The fix is derivable from the ASN's own content. T10a.6 (DomainDisjointness) already establishes that every `d ∈ E_doc` inhabits exactly one allocator's tracked domain, and the K.δ k=0 definition already permits document minting via sibling-increment on either `A_doc(·)` or `A_v(·)` chains. Reformulating the case-split to partition by owning allocator (rather than minting event) follows directly from these existing structural facts.

## Issue 2: Properties Introduced table omits `L' = L` from J2 and J3 frame conjuncts
Reason: Pure editorial alignment between the table entries and the body prose, which already includes the `L' = L` conjunct as part of the extended-state frame. No external evidence required.

## Issue 3: K.δ case (ii) k = 1 multi-version chain — Sub-allocator names interaction with the case-split issue
Reason: The clarification uses existing ASN concepts — K.δ k=0's allocator-agnostic precondition, FrontierEquivalence's three-premise chain, and T10a.6's domain disjointness — to reconcile the operational uniformity with allocator-tree provenance. All material is already in the ASN.

## Issue 4: K.μ~ admissibility clause (i) — redundancy not noted
Reason: The redundancy is a logical consequence of S8a (a per-state invariant in ExtendedReachableStateInvariants) combined with K.μ~-FIX (derived in the same section). Verifying or annotating the redundancy is purely an internal derivation check against the ASN's own dependency chain.

## Issue 5: Worked example "interior content replacement" — admissibility verification ordering
Reason: The reframing is to align the worked example's verification language with the K.μ⁻ amendment's own framing — the per-subspace suffix shape is forced by post-state invariants, not a separate precondition. Both the amendment text and the K.μ⁻ precondition list are present in the ASN.
