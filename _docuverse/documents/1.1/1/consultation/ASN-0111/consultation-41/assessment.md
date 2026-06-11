# Channel Assignment — ASN-0111 review-41

**Date:** 2026-06-10 23:22

## Issue 1: wp derivation reasons from a prose postcondition whose well-formedness is asserted, not exhibited
Reason: The fix is a formalization of material already present in the ASN — the definition of `readlink` and the membership guard are both stated, so rewriting the postcondition as `a ∈ dom(Σ.L) ∧ result = Σ.L(a)` and redoing the wp step by substitution requires no design intent or implementation evidence.

## Issue 2: RL5 carries a defensive parenthetical that re-litigates its relation to RL0 instead of advancing the claim
Reason: The fix is a pure deletion of meta-prose; the review confirms the preceding sentence already carries the full derivation, so no external channel is needed.

## Issue 3: RL4 closes with a forward-reference inventory of what the worked read does and does not prove
Reason: The fix is a pure deletion of a forward-reference parenthetical; the two-state witness lives in RL4's own paragraph and the worked read self-describes correctly, so the change is verifiable from the ASN alone.
