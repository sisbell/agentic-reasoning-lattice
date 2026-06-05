# Channel Assignment — ASN-0103 review-1

**Date:** 2026-06-04 18:09

## Issue 1: The document-frontier formula `d = inc(max(D_A), 0)` selects version addresses and collides with future version allocations
Reason: The collision and the structural fix (restrict `D_A` to length `#A+2`) are fully derivable from foundation results already cited (version fork `inc(d_src,1)`, length characterization, T1, T10). Gregory is consulted only to confirm the corrected non-collision claim matches how the real allocator computes the document frontier.
Gregory question: When CREATENEWDOCUMENT allocates the next document address under an account, does udanax-green scan all child entities (versions included) or advance a dedicated document-chain frontier that excludes version addresses?

## Issue 2: Freshness/ordering of `A_doc(A)` emissions is justified by foundation lemmas scoped to content/link sub-allocators
Reason: The fix is a citation correction — the needed strict-increase and disjointness/uniqueness properties for the SiblingStream `A_doc(A)` are derivable from S0 and B7/B8, both already in the foundation the ASN references.

## Issue 3: CND.monotone's cross-allocator ordering is not established by T9
Reason: The fix replaces the T9 appeal with an explicit T1 lexicographic comparison at position `#A+2`; the reviewer already supplies this argument and all premises (T1, allocator structure) are present in the ASN's foundation.

## Issue 4: No concrete worked example verifying the post-state
Reason: The worked example is a direct application of the ASN's own (corrected) allocation formulas and post-state contract; no design intent or implementation evidence is required to trace it.

## Issue 5: The ownership transfer `ω_{Σ'}(d) = ω_Σ(A)` is asserted with a one-line derivation
Reason: The fix is to make an internal derivation explicit by invoking already-named foundation results — the E↔B coupling (O17b/O18) and the account-tier boundary (O1a) — then applying the `ω` definition from ASN-0042; all premises exist in the cited foundation.
