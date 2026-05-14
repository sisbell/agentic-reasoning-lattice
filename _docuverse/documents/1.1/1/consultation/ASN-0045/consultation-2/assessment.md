# Channel Assignment — ASN-0045 review-2

**Date:** 2026-05-13 21:52

## Issue 1: ValidAddress is undefined notation
Reason: Pure terminological fix — replace `ValidAddress(t)` with `T4-valid(t)` citing T4. Derivable from the ASN's existing foundation citations.

## Issue 2: Foundation T4c already defines these labels
Reason: Fix is to cite T4c (LevelDetermination) and express the four labels as consequences/renamings of T4c's labels. T4c is a foundation ASN already in the dependency stack; no external evidence needed.

## Issue 3: Unjustified rename from T4c's "user" to "account"
Reason: Choosing between "user" and "account" requires both design intent (was "account" the intended term?) and implementation evidence (the review itself cites `tumbleraccounteq` as a signal — Gregory can confirm which term the code uses).
Nelson question: In Literary Machines and the concept notes, does Nelson refer to the zeros(t)=1 level as "user" or "account" (or some other term), and is there design intent that distinguishes the two?
Gregory question: In udanax-green, does the code at the zeros(t)=1 hierarchy level use "user", "account", or some other terminology (e.g., in `tumbleraccounteq`, baptism routines, identifiers)?

## Issue 4: Well-definedness of the labelling is asserted, not derived
Reason: The exhaustion + pairwise disjointness postcondition is exactly T4c's existing result; the fix is a citation and one-line postcondition. Internal to the foundation stack.

## Issue 5: No concrete example
Reason: Example construction follows mechanically from T4 validity and the zero-count convention; any T4-valid tumbler with k zeros illustrates level k. No external evidence needed.
