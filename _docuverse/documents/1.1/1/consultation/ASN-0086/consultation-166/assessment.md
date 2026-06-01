# Channel Assignment — ASN-0086 review-166

**Date:** 2026-06-01 06:31

## Issue 1: Nullify's P1/P2 are presented as preconditions in the Properties table but as non-gating in the body
Reason: Internal consistency fix — the body already establishes that only P0 (`d_retr ∈ dom(Σ.M)`) gates emission, with P1 as a postcondition-establishing condition and P2 as a scope label. Reconciling the Properties table with the body's own contract requires no design intent or implementation evidence; the gating analysis is fully present in the ASN.

## Issue 2: Non-fixpoint semantics of retraction-of-retraction stated twice in the same property
Reason: Pure editorial deduplication of the audit-slice mechanism between R6b's body and its Remark; the reasoning is entirely contained in the ASN and no external channel bears on whether two paragraphs restate one mechanism.

## Issue 3: Worked sketch attributes L2/L11a/L12b discharge to "R0's generic argument," outside R0's scope
Reason: The fix turns on whether L2/L11a/L12b belong to ASN-0043's `StateLocalInvariants` catalog or are lemma-consequences — a matter settled by ASN-0043's own definitions, which the review already characterizes (L2 from `home`, L11a = GlobalUniqueness instantiated, L12b from L12a+L1a). Verifiable against the foundation ASNs without design-intent or implementation input.
