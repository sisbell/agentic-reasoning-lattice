# Channel Assignment — ASN-0043 review-100

**Date:** 2026-05-30 13:37

## Issue 1: "TA5a is unconditional for k ∈ {0, 1}" is false — TA5a is unconditional only for k = 0
Reason: The fix is internal — TA5a's exact bound (`k = 1 ∧ zeros(t) ≤ 3`) is the cited ASN-0034 foundation, and the ASN already supplies `zeros(input) = 3 ≤ 3` at both occurrences, so the correct discharge replaces the false premise without any external evidence or intent.

## Issue 2: L7's proof is a self-referential word-search rather than a structural argument
Reason: The fix is internal — recasting L7's justification as "the invariants constrain slot identity only up to positional distinctness" follows directly from L6 (SlotDistinction) already present in the ASN; no design-intent or implementation evidence is needed since the structural claim is about the existing invariants' own quantification.
