# Channel Assignment — ASN-0130 review-21

**Date:** 2026-06-13 03:53

## Issue 1: Front-matter re-derives PR1 and PR2 rather than pointing to them
Reason: Pure editorial consolidation — the intro and commitments slots duplicate conclusions (validation-split, DAG/termination) that PR1 and PR2 already fully establish in the body. The fix is to thin the previews to dependency-plus-pointer and leave the arguments where they live; no design intent or implementation evidence is at stake, only the note's own prose structure.

## Issue 2: De-registration narrative and the Open-question-3 deferral repeated across PR1, PR3, and PS2
Reason: Editorial de-duplication internal to the note — the "withdraws the endorsement, not the artifact" point and the OQ3 deferral are already stated in PR1/PR3, and the fix is to have PS2 cite rather than restate and to voice OQ3 once. All the substance is present in the ASN; nothing about design intent or the implementation needs consulting.
