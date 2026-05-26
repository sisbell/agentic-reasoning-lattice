# Channel Assignment — ASN-0099 review-1

**Date:** 2026-05-26 16:16

## Issue 1: No concrete worked example
Reason: Building a small concrete state and walking the operation through it is purely internal scaffolding — all needed structure (arrangement, endset coverage, slot indexing) is established by the ASN and its cited foundations (0043, 0047, 0058, 0093).

## Issue 2: F2 and F3 stated as obligations but not derived
Reason: The derivation is a tautology of the set-comprehension definition given in the ASN itself; no external channel needed.

## Issue 3: Preconditions on `image` left implicit
Reason: Stating the preconditions `d ∈ dom(Σ.M) ∧ R ⊆ dom(Σ.M(d))` is internal cleanup. The deeper question of whether the operation should be total over arbitrary V-input or guarded by precondition is parallel to the already-open question about out-of-domain I-sets and can be deferred to Open Questions in the same idiom.

## Issue 4: `*` notation conflicts with the filter framework
Reason: This is a formal-coherence issue within the ASN's own definitions of `findlinks` (existential over slots) vs. `findlinks_filtered` (universal over constraints). Resolvable by tightening the prose without external input.

## Issue 5: F10 OrderedResult requires finiteness, not derived
Reason: Finiteness follows from `result ⊆ dom(Σ.L)` plus L-fin (ASN-0093); T1 trichotomy (ASN-0034) gives the total order. Pure citation of already-cited foundations.

## Issue 6: Empty-query boundary case not addressed
Reason: Mechanical specialization — `coverage(e) ∩ ∅ = ∅` and `image(∅, d, Σ) = ∅` collapse F2/F3/F8/F13 to trivial identities. No design choice involved.

## Issue 7: F8 Determinism proof too brief
Reason: Each step (domain equality → pointwise equality → per-slot equality → coverage equality → match equality → set equality by extensionality) is a routine unfolding of definitions in the ASN. Internal proof expansion.

## Issue 8: F7 Endset symmetry not stated or derived in prose
Reason: Both halves ("slots equally searchable", "filters conjoin") follow directly from the quantifier structure of `matches` and `findlinks_filtered` as defined in the ASN. Internal.

## Issue 9: Link-subspace V-positions in `image` not addressed
Reason: That the operation works uniformly on link-subspace V-positions follows from S3★ (ASN-0047, image lands in `dom(Σ.C) ∪ dom(Σ.L)`) and L4 (ASN-0043, endsets may reference link-subspace addresses). Pure structural acknowledgment using existing dependencies.

## Issue 10: Creation-order recovery claim not derived
Reason: The discharge requires only citing SubAllocatorAxiom.ChainDiscipline and ChainEnumerationInjectivity (both in ASN-0093) — foundation lemmas already in scope. Internal citation fix.
