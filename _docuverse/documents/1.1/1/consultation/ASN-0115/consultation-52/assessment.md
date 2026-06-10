# Channel Assignment — ASN-0115 review-52

**Date:** 2026-06-10 05:14

## Issue 1: Rationale explains a vacuous firing direction of the override
Reason: Internal. The fix is pure deletion of a no-op clause; the reviewer's own justification — that the too-deep direction is already empty by Confinement — is a lemma present in the ASN, and the instruction to retain the too-shallow rationale is given. No design intent or implementation evidence is in question.

## Issue 2: Use-site forward references in the spec-set definition
Reason: Internal. Removing the "below"-pointing tails is structural, and the correct characterization the reviewer prescribes — that `item`'s totality rests on S3★-aux applied to active positions — is already established in the ASN's own `item` definition, so the rewrite needs nothing external.

## Issue 3: act-definition prose previews R6
Reason: Internal. The fix drops a gloss that duplicates R6, which the ASN already states formally; letting the `act` set-equation stand alone requires no design intent or implementation evidence.
