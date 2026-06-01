# Channel Assignment — ASN-0086 review-119

**Date:** 2026-05-31 22:57

## Issue 1: R7a's "absent clause (b)" branch contradicts its own hypothesis, is unproven, and is false
Reason: The fix is to delete a self-contradictory hedge whose case the stated hypothesis ("substrate-conforming layer," which by its own Definition entails clause (b)) already excludes. The contradiction and falsity are both established from the ASN's own definitions and the existing non-conformance witness — no design-intent or implementation evidence is needed.

## Issue 2: The "single-depth" content of R6b is not in its formal contract
Reason: The fix is a formalization choice — either rewrite the formula to assert nullification holds even when the witness `b` is itself nullified, or fold persistence into R6a and demote single-depth to a definitional remark. Both options are derivable from the existing Definition of `nullified` and R6a's content already present in the note.

## Issue 3: Repeated restatement of the "at most one fresh key per home per step" discipline
Reason: Pure de-duplication — state the invariant once in the substrate-conforming-state Definition and cite it from R0a-Cor1 and R7a. Entirely an editorial restructuring of existing material.

## Issue 4: state-local-conforming definition justifies its shape by downstream consumers
Reason: The fix relocates use-site justification out of the definition and into the WP analyses that consume it, preserving the four-way containment and separating witness. This is internal editorial restructuring of content already in the note.
