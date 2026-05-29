# Channel Assignment — ASN-0053 review-38

**Date:** 2026-05-28 20:27

## Issue 1: Singleton-impossibility argument in S7 is proved for only one width
Reason: The missing step (no valid width yields reach = t.0, since the immediate successor requires ℓₖ = 0 at the action point, contradicting T12's ℓ > 0 requirement) is a pure arithmetic consequence of T12 and tumbler arithmetic already in ASN-0034/0053. No external channel needed.

## Issue 2: S8 derives N1's strict inequality from a justification that only yields ≤
Reason: The corrected justification (strictness comes from the emit condition `start(σᵢ) > r ≥ s`) is already present in the construction itself; this is an internal restatement using the proof's own machinery.

## Issue 3: WR is introduced but never invoked; downstream proofs re-derive it inline
Reason: Whether to cite WR or drop it in favor of D2 is an editorial consolidation decision fully internal to the note's own properties (WR, D2, S4a, S3b, S9).

## Issue 4: Mutual cross-reference between the reach-function section and S6
Reason: Removing reciprocal document-ordering pointers and stating the fact once is pure prose editing within the ASN; no design intent or implementation evidence is at issue.

## Issue 5: S6 closes with a defensive restatement of the precondition's purpose
Reason: Deleting the trailing restatement is a prose fix; the worked [1, 3, 0, 1] counterexample already in the note carries the point. Internal.
