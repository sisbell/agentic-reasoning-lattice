# Revision Categorization — ASN-0063 review-22

**Date:** 2026-03-22 02:24



## Issue 1: CL0 proof ends ∎ before establishing the element-level equality claim
Category: INTERNAL
Reason: The proof content for element-level tightness already exists in the ASN — it just needs to be moved inside the ∎-delimited proof or split into a corollary. No external evidence is needed.

## Issue 2: CL0 proof applies "convex" to a non-convex intersection
Category: INTERNAL
Reason: The review identifies that "convex in T" is the wrong characterization and supplies the correct one ("contiguous sub-range of V(β)"). The fix is a wording change using reasoning already present in the proof.

## Issue 3: ExtendedReachableStateInvariants base case omits D-CTG and D-MIN
Category: INTERNAL
Reason: D-CTG and D-MIN hold vacuously at Σ₀ since all arrangements are empty. The fix is adding two sentences of explicit verification using definitions already in the ASN.
