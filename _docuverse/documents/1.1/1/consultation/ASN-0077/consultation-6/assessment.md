# Channel Assignment — ASN-0077 review-6

**Date:** 2026-05-25 16:29

## Issue 1: O2 case split exhaustiveness not justified
Reason: Pure citation fix — S3★-aux (ASN-0047) is the foundation invariant that delivers exhaustiveness, already part of the cited foundation. No design intent or implementation evidence is needed; the fix is to add the citation at the case-split step.

## Issue 2: O0 (b) "sole modifier" framing rests on a wording that is not literally true
Reason: The auditor has already identified which transitions explicitly carry `L' = L` in their frame clauses and which do not. Both proposed reword paths (per-transition effect-clause check, or grounding entirely on L1c) operate on foundation material already cited in the ASN. Internal fix.

## Issue 3: Singleton I-span #b > #a case omits allocator-identification chain
Reason: The fix is to make explicit the chain S7a (ASN-0036) → SubAllocatorAxiom (a) (ASN-0047) → `A_C(d)` as `a`'s producing allocator. Both citations are already in the foundation references; the gap is rhetorical compression, not missing knowledge. Internal fix.

## Issue 4: O3 V-span sub-claim treats `origin(M(d)(v))` as well-defined without discharging domain membership
Reason: Citation fix — S3★ (ASN-0047) is what discharges `M(d)(v) ∈ dom(C) ∪ dom(L)`, and the ASN already invokes it at the analogous step in O7. The fix is to add the same citation in O3's V-span derivation. Internal.
