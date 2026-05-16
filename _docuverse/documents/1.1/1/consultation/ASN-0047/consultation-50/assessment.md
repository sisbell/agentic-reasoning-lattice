# Channel Assignment — ASN-0047 review-50

**Date:** 2026-05-16 15:50

## Issue 1: Notation inconsistency in ExtendedReachableStateInvariants theorem statement
Reason: Pure notation fix — the ASN already establishes D-CTG★/D-MIN★ as the per-subspace forms and notes "all subsequent references to D-CTG and D-MIN in this ASN denote the amended forms." Reviser just needs to make the theorem statement consistent with that aliasing convention.

## Issue 2: K.μ~ redundancy argument's conclusion is weaker than its claim
Reason: The fix turns on whether the abstract model takes a uniqueness invariant on link-subspace mappings within a document. Need Nelson for design intent (can the same link appear at two link-arrangement positions in its home document?) and Gregory for whether the implementation enforces or admits such duplication.
Nelson question: Does the design intend that each link in a document's link subspace appear at exactly one V-position — i.e., is link-arrangement multiplicity within a single home document constrained to ≤1, or may the same ℓ be placed at multiple link-subspace V-positions?
Gregory question: Does the udanax-green link-arrangement protocol (e.g., the link-placement pathway invoked alongside `docreatelink`) prevent a single link ISA from being mapped to more than one VSA within the same document, or can the same link appear at multiple link-subspace positions?

## Issue 3: K.δ k=1 case for non-document entities is unspecified
Reason: Whether the design admits "account versions" or "node versions" is a question about Nelson's intent, and whether the implementation supports them is a question about Gregory's protocols. Without either evidence channel, this ASN cannot decide between admit/restrict/defer.
Nelson question: Does the Xanadu design contemplate versioning at the account level or node level — i.e., are addresses of the form `[N,0,U,1]` (account-shaped sibling at deeper tumbler depth) or analogous node-level extensions intended as "account versions" or "node versions," or is versioning reserved to documents alone (LM 4/29)?
Gregory question: Does udanax-green provide any account- or node-level analog of `docreatenewversion` (do1.c:271) — i.e., does any FEBE/BEBE operation produce account-shaped or node-shaped addresses via depth-1 tumbler extension from an existing account or node address?

## Issue 4: ExtendedReachableStateInvariants proof omits explicit P8 check for K.δ
Reason: Internal fix — P8 is defined in this ASN, K.δ's preconditions are stated in this ASN, and the preservation argument is already sketched in P8's derivation paragraph. Reviser just adds the missing sentence at the proof site.

## Issue 5: K.μ⁻ admissibility for the link subspace is not exercised in any worked example
Reason: Internal fix — the admissibility derivation (cases (a)/(b)/(c)) is fully established in the ASN's K.μ⁻ definition, and the worked example uses already-defined transitions on already-introduced concrete tumbler values. No external evidence needed to construct the example.

## Issue 6: L3 amendment's downstream consequences are unstated
Reason: The collapse of `same_type` on empty-Θ links is a downstream-equivalence question rooted in ASN-0043's L8/L10. Need Nelson for whether untyped links were designed to share a degenerate type-class, and Gregory for whether the implementation's type-matching pathway handles empty Θ specially.
Nelson question: When a link is created without a type-endset (empty Θ), does the design intend it to participate in type-matching equivalence (all untyped links sharing a trivial type-class), or to stand outside the type-matching relation entirely?
Gregory question: How does the udanax-green type-matching machinery (e.g., the `same_type` pathway used by typed link queries) treat a link with an empty type-endset — does it skip such links, return false on all comparisons, or treat all empty-Θ links as equivalent?

## Issue 7: Allocator hierarchy claim's cross-document disjointness leans on T10 without explicit instantiation
Reason: Internal fix — T10a.6 (DomainDisjointness) and T10 (PartitionIndependence) are both in ASN-0034, and K.δ's allocation discipline in this ASN supplies the non-nesting of distinct document addresses. Reviser just chains the existing results explicitly.
