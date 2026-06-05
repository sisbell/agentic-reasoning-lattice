# Channel Assignment — ASN-0100 review-87

**Date:** 2026-06-05 06:06

## Issue 1: K.μ⁻ strict-contraction precondition is asserted, not discharged
Reason: Internal — the fix chains (INS.μ⁻-fires)'s `Right ≠ ∅` to `p_m ≤ N = n_{s_C}` and the decomposition's own `n'_{s_C} = p_m − 1`, all already present in the ASN. No design intent or implementation evidence needed.

## Issue 2: Repeated forward deferral to the same downstream section
Reason: Internal — the S8a/depth check on `shift(p,k)` is a two-line OrdAddHom + TumblerAdd result-length argument using ASN-0034/0082 already cited in the ASN. Restructuring, not new evidence.

## Issue 3: Anticipatory block-algebra bridge misplaced in Effect One
Reason: Internal — relocating the `⟦(p, a_0, n)⟧` denotation sentence to §Per-subspace span decomposition is purely organizational; both sites already exist in the ASN.

## Issue 4: Redundant restatement in the re-insertion example
Reason: Internal — deleting a sentence that duplicates step 1 of the same example requires no external input.
