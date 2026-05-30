# Channel Assignment — ASN-0036 review-193

**Date:** 2026-05-29 23:29

## Issue 1: OrdShiftHom's contract does not supply the last-component value the derivation uses
Reason: Internal. The required component-value formula (`shift(v,n)ₘ = vₘ + n`) is already established in OrdShiftHom's own proof body and traces to OrdinalShift (ASN-0034), which is already cited elsewhere in the note; the fix is a citation/contract adjustment derivable from existing content.

## Issue 2: OrdShiftHom is introduced by its downstream use rather than its content
Reason: Internal. The lemma's content (subspace preservation and S8a-preservation under shift) is already stated in its formal contract and proof; the fix is purely a rewording of the introductory sentence.

## Issue 3: Defensive justification inside the S5 construction
Reason: Internal. The fix is deleting a trailing justification clause; the distinctness argument it surrounds is self-contained within the proof.
