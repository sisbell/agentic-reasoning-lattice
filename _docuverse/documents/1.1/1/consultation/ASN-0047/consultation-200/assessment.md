# Channel Assignment — ASN-0047 review-200

**Date:** 2026-06-01 02:36

## Issue 1: ParentAllocatorDispatch is proven only for `A_v(d)` but invoked for account-level allocators
Reason: The fix is internal — the missing identification step (that an account's unique T10a.6 owning allocator is `A_account(parent(t))`) follows from the ASN's own K.δ k=2 construction (each non-node entity enters E only via a tracked sub-allocator inc-step, per TrackedEmission and case (ii)) plus T10a.6 disjointness, so generalizing the lemma's case analysis to all entity-hierarchy levels is derivable from material already present.

## Issue 2: The "depth is re-pinned after clearance" claim is stated three times in near-identical prose
Reason: Pure editorial deduplication — consolidating the live-depth re-pinning rule at the `m_L(d)` definition and back-referencing it elsewhere requires no external input.

## Issue 3: Forward-reference deferral cluster in the K.μ~ admissibility argument
Reason: Pure expository restructuring — stating the filter-vs-non-vacuity framing once at the section head is derivable from the reasoning already in Steps (A), (B), and the necessity/sufficiency proof; no channel needed.
