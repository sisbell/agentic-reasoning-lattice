# Revision Categorization — ASN-0029 review-5

**Date:** 2026-03-11 11:24

## Issue 1: D1 and D12(g) — per-account monotonicity is false
Category: INTERNAL
Reason: The counterexample is constructible entirely from T1, T9, and T10a as already defined. The fix (split by case, restate as per-allocator) follows from existing definitions.

## Issue 2: account(d) uniqueness claim is false
Category: INTERNAL
Reason: The prose already states the correct answer ("the N.0.U portion"); the formal definition just needs to be aligned with it using `max≼` or `fields()`, both already available.

## Issue 3: D14 closure assumes D0 creates root documents, unstated
Category: INTERNAL
Reason: The implicit reasoning (D0 uses T10a's root allocator, producing single-component document fields) is derivable from the existing allocator discipline definitions. The fix is to make explicit what's already implied.

## Issue 4: D4 cites T8 for document address permanence, but T8 governs I-space
Category: INTERNAL
Reason: A citation error — the correct justification (pure function of an immutable value, membership permanent by D2) is already present in the ASN's own definitions.

## Issue 5: D13 Case 1 does not verify the child allocation produces a document-level address
Category: INTERNAL
Reason: The constraint `k' = 1` is derivable from the requirement that `d_v` be a document (`zeros = 2`), combined with TA5(d)'s specification of how `inc(·, k')` affects zero count. No external evidence needed.

## Issue 6: D0's monotonicity depends on D0 being root-only (circular with Issue 3)
Category: INTERNAL
Reason: Same gap as Issue 3 — the fix is identical (make root-only allocation explicit in D0), and the justification comes from the same existing T10a definitions.
