# Channel Assignment — ASN-0047 review-308

**Date:** 2026-06-02 00:44

## Issue 1: Forward-reference accretion around ValidComposite★ — duplicated skeleton and repeated deferrals
Reason: Purely editorial restructuring — collapsing a duplicated skeleton and repeated deferrals to a single bare reference. No design intent or implementation evidence is involved; the fix is internal.

## Issue 2: J4 step (ii) invariant-discharge list omits S8★ and D-SEQ★
Reason: The omitted invariants and their derivations already exist in the ASN — D-SEQ★ follows from the listed shape invariants and S8★(s_L) is vacuous since V_{s_L}(d_new) = ∅. The fix is derivable from the ASN's own content.
