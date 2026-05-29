# Channel Assignment — ASN-0040 review-56

**Date:** 2026-05-28 22:16

## Issue 1: The same B4 read-consistency claim is deferred three times
Reason: Pure restructuring — state the read-against-precondition-state semantics once in B4 and have the other two sites cite it. The fact and its locations are all present in the ASN.

## Issue 2: Bop precondition slot carries proof-bookkeeping essay
Reason: Editorial reduction to a single clause; the §B1/§B10/§B_fin proofs already carry the reasoning. Internal.

## Issue 3: B6 has a redundant summary that previews its own proof
Reason: Deletion of a sentence already covered by the preceding per-condition analysis and the proof itself. Internal.

## Issue 4: B4 leaks an implementation/concurrency rationale
Reason: Removing or de-normalizing the serialization-grain sentence is internal; B4's actual content (single atomic edge) and B7's disjointness are both already in the ASN, so no external evidence is needed to scope it.

## Issue 5: B8 prose paragraph duplicates the B8 proof
Reason: The preview paragraph and the Case 1/Case 2 proof are the same content already in the ASN; dropping or compressing one is internal.

## Issue 6: B0a restates B6 before B6 is defined
Reason: Replacing the verbatim restatement with a forward reference to B6 is purely internal cross-referencing.

## Issue 7: "not addressable" overclaims in B3
Reason: The fix is a terminology correction the ASN's own framing supports — T1 totally orders all of T, so every tumbler is a valid address. Derivable internally.

## Issue 8: B7/B8/S0 substantially re-derive foundation results without acknowledging the parallel
Reason: Choosing between "cite T10a and explain why a registry-level restatement is needed" versus "build on T10a directly" depends on whether baptism *is* the allocator discipline or a genuinely distinct layer — a design-intent question (Nelson) and an implementation-fact question (Gregory) the ASN itself defers via the `allocated(s) ⊆ s.B` open question.
Nelson question: Was baptism intended as the same mechanism as per-allocator address allocation, or as a distinct registry-level layer sitting above it?
Gregory question: Does udanax-green use one shared mechanism for address allocation and baptismal commitment, or two separate ones with the allocator feeding a distinct registry?
