# Channel Assignment — ASN-0070 review-2

**Date:** 2026-05-25 12:18

## Issue 1: Postcondition strict equality is too strong
Reason: The fix is a notational correction — defining a V-restricted denotation or restating as intersection equality. Derivable from ASN-0053's existing `⟦·⟧` definition and the depth constraints already cited (S8-depth, LinkVPositionDepthAxiom).

## Issue 2: Contiguity proof's TS5 citation doesn't cover k₁ = 0
Reason: The fix adds a citation to TS4 + OrdinalShiftBase for the boundary case. Both claims exist in ASN-0034 and are mechanical to invoke.

## Issue 3: V-subspace / I-subspace correspondence not derived
Reason: The correspondence derives from S3★ (ASN-0047) and L0 (ASN-0047), both already cited. Open question 6's resolution follows mechanically from the derivation.

## Issue 4: F-multi proof is over-engineered
Reason: Internal proof restructuring — separating admissibility (S5) from implication (definition of R). No external evidence needed.

## Issue 5: F-empty derivation not shown
Reason: The derivation chain uses only the inverse-image definition and canonical-form assumption already in the ASN. The last step (`⟦·⟧ = ∅ ⟹ ⟨⟩`) is derivable from S9's normalization uniqueness.

## Issue 6: F-canonical uniqueness not derived
Reason: Each step in the chain (S8-depth, LinkVPositionDepthAxiom, S9, external ordering) is already cited or stated. Mechanical expansion.

## Issue 7: F-det derivation chain not formalized
Reason: All dependencies (S2, S3★-aux, S9) are listed; the fix composes them into an explicit inference chain. No new evidence required.

## Issue 8: F-sound/F-complete categorization conflicts with role
Reason: This is a documentation-structure decision (LEMMA vs. OBLIGATION classification). The ASN's own postcondition determines the answer — F-sound/F-complete are the two halves of the set-equality, hence LEMMA-derivable. Internal.

## Issue 9: Open question already answered in body
Reason: The Slot Uniformity section already resolves this. Internal consistency fix — either remove the question or qualify the body.

## Issue 10: F0 and F1 not labeled in body
Reason: Pure formatting fix — add parallel `### F0 — ...` and `### F1 — ...` headings to match the other claim presentations.
