# Channel Assignment — ASN-0047 review-207

**Date:** 2026-06-01 03:47

## Issue 1: Admissibility-filter prose explains the clause's epistemic status rather than advancing it, and is restated three times
Reason: Purely editorial — the fix removes duplicated epistemic-status framings and lets the existing Steps (A)/(B) carry the reasoning. No design intent or implementation evidence is needed; the clause's role is fully fixed by the ASN's own structure.

## Issue 2: S8★ "strictly weaker than S8" stated twice within its own definition
Reason: Internal deduplication — keep the first statement of the (a)/(b)-carries, (c)-drops characterization and delete the restatement. Entirely derivable from the ASN's own S8★ definition.

## Issue 3: Implementation-rationale parentheticals in abstract slots
Reason: Editorial — drop the implementation parenthetical (the abstract live-depth rule is already fully specified) and consolidate the repeated "(with zero intermediate 1s at m = 2)" asides into one forward note at D-SEQ★. The instruction is to remove, not verify against the implementation, so no channel is required.
