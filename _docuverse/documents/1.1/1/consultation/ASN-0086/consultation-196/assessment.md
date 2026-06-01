# Channel Assignment — ASN-0086 review-196

**Date:** 2026-06-01 14:13

## Issue 1: Non-monotonicity of `A_K` cites the wrong worked-sketch step
Reason: Fully internal — the ASN's own Worked Sketch arithmetic (Steps 1 and 2) supplies the correct witnesses, and the fix is a citation correction derivable from the note's existing content. No design-intent or implementation evidence is needed.

## Issue 2: Repeated deferrals to the same downstream location (anti-bloat)
Reason: Purely editorial — removing redundant back-references to an already-proved strictness fact and an internal forward pointer requires no external input, only rewording within the note. The supporting facts are all established at their home sites in the ASN.
