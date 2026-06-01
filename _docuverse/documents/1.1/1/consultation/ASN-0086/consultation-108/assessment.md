# Channel Assignment — ASN-0086 review-108

**Date:** 2026-05-31 20:48

## Issue 1: ConformingHomedContiguity induction step only covers single-key extension, but R7a admits multi-key composite transitions
Reason: Clause (b) is the ASN's own definition of substrate-conforming states/layers; the fix is to either extend the induction or sharpen clause (b) to require simultaneously-emitted same-home keys to fill the next contiguous chain segment. Both options are within the author's definitional control and derivable from the existing frontier-emission framing.

## Issue 2: No worked example exercises R7a's multi-key-same-home replay path
Reason: Adding a composite-emission worked example only re-applies machinery already proved in R7a discharge (4)(iii) and the chain recurrence; the concrete tumbler trace is mechanical given the ASN's own allocator structure.

## Issue 3: Nullify P1 labeled both "does not gate emission" and "executing precondition"
Reason: The contradiction is resolved internally — WP Case 1's necessity argument already establishes that P1 is needed only for the `a ∈ nullified(Σ')` postcondition, not for emission, so the author picks the non-gating classification and rephrases the composition clause accordingly.

## Issue 4: Repeated "derives from clause (b), not the →-scoped ChainMembershipForOrigin" justification (anti-bloat)
Reason: Pure prose deduplication — state the scope justification once at the sub-lemma and cite by name at consumers; no external evidence or design intent required.
