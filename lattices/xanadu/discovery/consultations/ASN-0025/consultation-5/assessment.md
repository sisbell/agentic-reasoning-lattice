# Revision Categorization — ASN-0025 review-5

**Date:** 2026-03-07 08:34

## Issue 1: P6 derivation assumes an unstated equivalence between Σ.D and orgl
Category: INTERNAL
Reason: All three fix options are derivable from ASN content. Option (c) is immediate — every operation already states Σ'.D ⊇ Σ.D in its postconditions, so P6 follows by case analysis with no orgl argument needed.

## Issue 2: INSERT has no formal postcondition for new V-entries
Category: INTERNAL
Reason: The mapping of new positions to freshly allocated addresses b₁...bₙ is already described informally in the I-space and V-space effect sections. The fix is writing the formal statement that the text already implies.

## Issue 3: COPY V-space postconditions given by reference to INSERT
Category: INTERNAL
Reason: The COPY section already describes the shift mechanics and the fact that new entries map to source I-addresses from S. The fix is stating these as explicit formal postconditions rather than referencing INSERT.

## Issue 4: CREATE VERSION V-space postcondition is informal
Category: INTERNAL
Reason: The ASN already contains Gregory evidence that `insertpm` performs a position-for-position copy via `movetumbler`, and the Correspondence section relies on range equality. The stronger reading (position-for-position) is supported by existing evidence and implies the weaker; the fix is choosing and stating it formally.

## Issue 5: DELETE precondition does not declare its parameters
Category: INTERNAL
Reason: Parameters p and n already appear in the V-space effect postconditions. The fix is promoting them to the precondition block and stating the span-existence condition formally, mirroring INSERT's structure.
