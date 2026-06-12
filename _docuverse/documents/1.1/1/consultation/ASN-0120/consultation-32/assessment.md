# Channel Assignment — ASN-0120 review-32

**Date:** 2026-06-11 18:54

## Issue 1: MLop's two branch predicates are independent, and the divergent boundary is never checked
Reason: The fix is internal — the reviewer has already verified soundness of the mixed case from substrate facts the ASN cites (K.λ whole-store freshness from ASN-0093, the K.μ⁻ contracted-home state and D-MIN★/D-SEQ★ from ASN-0047); what remains is to state the predicate independence, name the divergent state, and record the verification, all derivable from material already in hand.

## Issue 2: Repeated forward deferrals to MLop carrying organizational meta-prose
Reason: Pure prose-accretion cleanup — deleting meta-organizational clauses and collapsing to one bare forward reference requires no design intent or implementation evidence.

## Issue 3: The empty-resolution boundary is settled once and then re-argued twice
Reason: Pure deduplication — the boundary fact is fully derived in the resolution section, and the fix is to delete the restatements in ML5/ML6 prose and let them cite the settled fact; no external input needed.
