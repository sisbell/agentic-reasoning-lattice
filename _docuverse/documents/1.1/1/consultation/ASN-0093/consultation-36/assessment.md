# Channel Assignment — ASN-0093 review-36

**Date:** 2026-05-31 07:23

## Issue 1: Frame preamble defends a redundant two-clause frame
Reason: Pure notational cleanup — replace the two-clause frame with `M' = M` and delete the explanatory preamble. Derivable from the ASN's own partial-function semantics; no design intent or implementation evidence at stake.

## Issue 2: Discharge-bookkeeping meta-prose on the per-chain disciplines
Reason: Deletion of meta-prose already subsumed by the CITATION status in the Properties table. Internal bookkeeping, no channel needed.

## Issue 3: Adequacy justification of the abstract stream
Reason: Removing a non-load-bearing defensive sentence (or silently folding the one fact into the emission rule) is an internal editorial choice within the note.

## Issue 4: Scope and Open Questions both point at the same deferred content
Reason: Consolidating two cross-references to one substantive sentence is a structural edit; the substantive content (L12's value-equality clause) is already present in the note.

## Issue 5: Content↔link prose duplicated where the "symmetric" device is available
Reason: Replacing duplicated sub-cases with the content↔link substitution device the note already uses elsewhere (L1c) is a purely internal restructuring of existing proof text.

## Issue 6: Freshness inventory in the precondition slot, with an imprecise citation
Reason: Both fixes — removing the duplicated inventory and correcting the L0→DisjointSubAllocatorChains citation — are resolved by the note's own discharge matrix, which already records the correct citation. Internal consistency repair.

## Issue 7: "Depends on no state component" restated repeatedly
Reason: Stating the state-independence of the tumbler projections once at the `origin(·)` definition and letting other slots cite it is an internal deduplication of a fact already asserted in the note.
