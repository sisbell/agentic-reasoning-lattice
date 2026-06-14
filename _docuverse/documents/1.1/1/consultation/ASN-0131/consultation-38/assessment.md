# Channel Assignment — ASN-0131 review-38

**Date:** 2026-06-13 22:32

## Issue 1: Global orphaning/resurrection digression in the contraction analysis
Reason: Internal. Dropping the trailing LP17/LP18 sentence is a scope trim — the contraction claim's correctness (region-local loss + re-surfacing) is already carried by F-IMG-CONTR, RE-CWP, and the surrounding prose; deciding that the global orphaning case lies outside a single-region query is a structural fact the ASN itself establishes, requiring no design intent or implementation evidence.

## Issue 2: Redundant clause in the ASN-0086 bridge
Reason: Internal. The review affirms the bridge is correct; the fix only deletes a clause that restates what "constrains `Σ.L` alone" already entails. That the empty-vs-populated arrangement distinction is definitionally irrelevant once the lemmas are `Σ.L`-only is derivable from the bridge argument already present in the note.

## Issue 3: Stability-section bookend recap and RE-IDENT forward pointer
Reason: Internal. This is a de-duplication edit — removing a forward pointer and a closing recap of the image-motion/population-motion split already enumerated in the section. No design intent or implementation fact is at stake; the trim is purely about prose redundancy within the note.
