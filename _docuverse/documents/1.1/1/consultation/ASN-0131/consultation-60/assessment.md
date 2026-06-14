# Channel Assignment — ASN-0131 review-60

**Date:** 2026-06-14 05:52

## Issue 1: Import-licensing infrastructure front-loaded before the central definition
Reason: Pure document reorganization — relocating the RE-ADDR derivation and the R0a/R-Scope/R6a citations to the "Composing regions"/"Stability" sections where they are consumed, and dropping the use-site-inventory sentence. All the material already exists in the note; nothing about design intent or implementation behavior is at issue.

## Issue 2: An excluded case explored inline, duplicating Open Question 7
Reason: Editorial deletion of an excluded-case walk-through. The `W ⊆ s_C` caller obligation is already fixed by the operation's own precondition, the content-disjointness point is already established in the surrounding paragraph, and OQ7 already carries the link-subspace question verbatim — so the fix is internal trimming.

## Issue 3: Permanence claim cites the single-step lemma, not the multi-step one
Reason: Citation correction within the spec's own formal apparatus — swap LP3 for LP3★ (MultiStepCoverageInvariance) in the prose and the RE-IDENT row, or make the per-step LP3 + induction explicit. The review already identifies the existing foundation lemma; which sibling-ASN lemma to cite is neither a design-intent nor an implementation-evidence question.
