# Channel Assignment — ASN-0086 review-249

**Date:** 2026-06-01 22:43

## Issue 1: Inconsistent symbol ⊀ used where the prefix-negation ⋠ is meant
Reason: Purely a symbol-consistency fix derivable from the note's own conventions (`⋠` is used for prefix-negation in Step 3 and the foundations); no design intent or implementation evidence is needed.

## Issue 2: `addr` codomain note states its surjectivity condition three times
Reason: Anti-bloat editorial collapse of a redundant restatement; the image expression already present in the definition makes the single-statement form immediate, so the fix is internal.
