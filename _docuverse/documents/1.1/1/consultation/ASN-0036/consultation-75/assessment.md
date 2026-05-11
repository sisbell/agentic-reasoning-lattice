# Channel Assignment — ASN-0036 review-75

**Date:** 2026-05-11 00:01

## Issue 1: D-CTG-depth proof duplication
Reason: Editorial restructuring — choose between deletion and reframing as preview. Fully derivable from the ASN's own organization.

## Issue 2: Missing Depends sections in lemma formal contracts
Reason: Metadata format consistency — the dependencies (TumblerAdd, TA0, OrdinalShift, OrdinalDisplacement) are already cited in the proof bodies and need only be surfaced into contract blocks.

## Issue 3: Inconsistent formal contract presentation
Reason: Formatting uniformity — every introduced property is already stated; the task is to wrap each in a Preconditions/Postconditions/Frame (or Axiom) block matching the existing style.

## Issue 4: S8 proof omits S7c citation for I-address subspace preservation under shift
Reason: Internal proof rigor — S7c is already established in this ASN; the fix is to cite it where the I-address shift parallel currently rests on TumblerAdd alone.

## Issue 5: Subspace function for I-addresses informal
Reason: Naming convention — define `subspace_I(a) = E(a)₁` (or overload `subspace`) using projections already supplied by T4b and the depth guarantee from S7c. No external input needed.

## Issue 6: OrdShiftHom S8a preservation as prose rather than formal postcondition
Reason: Formatting — the substantive claim is already proved; promote the S8a-preservation conclusion from prose into an explicit postcondition (b).

## Issue 7: Initial depth m mechanism not formally addressed
Reason: The choice between committing to a canonical m at the strand-model level versus delegating to operations turns on design intent. Gregory's depth-2 evidence is already in the ASN; Nelson's intent disambiguates whether depth-2 is architectural commitment or implementation convention.
Nelson question: Did the two-stream design require a fixed V-position depth (specifically m = 2 for the text subspace) as an architectural commitment, or was the depth choice deliberately left open to be fixed by allocation/insertion operations?
