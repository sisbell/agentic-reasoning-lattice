# Channel Assignment — ASN-0100 review-27

**Date:** 2026-06-03 09:40

## Issue 1: S8★ verification establishes existence but not condition (c) (uniqueness)
Reason: The review supplies the exact lemma to cite (M12, CanonicalUniqueness; ASN-0058) and states it shares M2's standing preconditions — all of which (S8-fin, S2, S3★|_{s_C}, S8a, S8-depth) are already verified in the post-state. The fix is to add the M12 citation and note the precondition reuse; no external evidence or intent is needed.

## Issue 2: ActivatedEmission omitted from the per-state invariant survey
Reason: The fix must place ActivatedEmission in the correct grouping and justify its preservation, but the ASN never defines it — its definition lives in ASN-0047's ExtendedReachableStateInvariants. The review asserts an `E' = E` frame justification, but whether that is sound depends on what ActivatedEmission actually quantifies over (entity set vs. content/link emissions touched by K.α); this is an implementation/synthesis fact for Gregory.
Gregory question: What does the ActivatedEmission invariant in ASN-0047's ExtendedReachableStateInvariants quantify over and constrain — does it range over the entity set E, or over content/link allocator emissions (dom(C)/dom(L)) that INSERT's K.α firings extend?
