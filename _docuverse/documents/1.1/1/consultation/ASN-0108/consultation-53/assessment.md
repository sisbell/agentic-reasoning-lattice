# Channel Assignment — ASN-0108 review-53

**Date:** 2026-06-13 11:35

## Issue 1: Key permanence is attributed to the wrong premises (S0/LP11, not L12)
Reason: Internal. The fix re-routes the permanence derivation through premises already cited in the ASN — coverage is "a combinatorial projection of its spans consulting no state component" (ASN-0043/0098, stated in the note's own opening) and the endset is immutable by L12 — so the corrected attribution follows mechanically from definitions already present; no design intent or implementation behavior is in question, only which stated premise the key actually reads.

## Issue 2: W9's local-fact paragraph re-narrates W8's computability-failure mechanism verbatim-in-substance
Reason: Internal. This is a pure deduplication edit — replace W9's restated computability-collapse mechanism with a citation to W8, keeping only W9's distinct cardinality content. No external fact is needed to decide what to cut.

## Issue 3: The resurrection/permanent-key fact and the clause-1-at-every-cursor condition are each stated twice across W5/W9/W9b with mutual deferral
Reason: Internal. This is a placement/cross-reference cleanup — consolidate the resurrection/permanent-key fact in W9b and the clause-1-at-every-cursor condition in W9b(i), then have W5 and W9 cite rather than restate. The logical content is unchanged and entirely within the note.

## Issue 4: The key introduction carries design-rationale forward-citing W5/W8 for a parameter that is explicitly not a claim
Reason: Internal. The fix trims the justificatory clause down to the structural fact (slice fixed a priori ⟹ key is a function of the immutable link value), which is already established in the same bullet; the legitimate spanfilade evidence stays as-is and the property-sorting moves to where W5/W8 already do it — no new implementation evidence or design intent required.
