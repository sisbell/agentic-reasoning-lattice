# Channel Assignment — ASN-0086 review-4

**Date:** 2026-05-16 16:34

## Issue 1: R0 Step 2 Case A — at-most-once violation when `d` has prior content allocations
Reason: The fix is derivable from the ASN's own content and its already-cited dependencies (ASN-0036 S7a/S7c on content allocation, T10a on allocator structure). The question is purely structural — whether `(d, 2)` is shared between content and link subspaces — and the answer is already determined by the cited axioms.

## Issue 2: Worked example concrete instantiation does not reconcile shared allocator structure
Reason: Downstream of Issue 1; resolution follows once Case A is restructured. The L1c chain semantics and shared `A_d` interpretation are already fixed by ASN-0036 and T10a as cited.

## Issue 3: R0 Step 4 L11a citation phrasing
Reason: Pure phrasing fix against L11a's actual statement (already cited from ASN-0043). Internal.

## Issue 4: R3 quantifier binds `K ∈ T_cat` rather than `T_admissible`
Reason: Quantifier correction using definitions established in this ASN. Internal.

## Issue 5: R6c stated single-step, prose claims multi-step
Reason: Statement/proof consistency fix using `⊑` (defined in this ASN) and R6a (just proved). Internal.
