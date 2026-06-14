# Channel Assignment — ASN-0133 review-34

**Date:** 2026-06-14 09:26

## Issue 1: The H-RF/H-W relationship is argued in full, then restated three more times
Reason: Purely editorial deduplication. The separation argument and all its content (H-W ⟹ H-RF, converse via Q5a, starvation defeats H-W) are already fully present in the note; collapsing the three restatements to back-references and stripping the downstream-consumer enumerations from the definitions requires no design intent or implementation evidence — only the note's own reasoning.

## Issue 2: Q0 states the members/targets_of/M_K default-value treatment twice
Reason: Purely editorial deduplication. The classification (these three atoms are both view-parameterized and UV-rewritten, taking the PC3 rebuild for audit/active and the UV filter for default) rests on ASN-0129's already-cited PC3/UV machinery; deleting the preview and keeping the full statement is internal to the note.

## Issue 3: PC4 miscited as the warrant for value-preservation across the rewrite
Reason: This is a citation-correctness question about the formal semantics of PC3/PC4/UV, all defined in the already-cited dependency ASN-0129. What PC4 (purity, single-term determinism) versus PC3+UV (cross-view value equality of distinct terms) each warrant is fixed by those rules' definitions; the reviewer's analysis already pins the correct premise, so the fix is derivable from the note and its dependencies without design intent or implementation evidence.
