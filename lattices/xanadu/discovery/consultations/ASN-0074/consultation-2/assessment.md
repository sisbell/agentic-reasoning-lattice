# Revision Categorization — ASN-0074 review-2

**Date:** 2026-03-22 15:06

## Issue 1: Worked example invokes M16 without establishing distinct origins
Category: INTERNAL
Reason: The fix is to explicitly state `origin(a) ≠ origin(b) ≠ origin(c)` in the worked example setup. M16's requirements are already defined in ASN-0058; the example just needs its assumptions tightened to match the property it invokes.

## Issue 2: Width preservation observed but not proved
Category: INTERNAL
Reason: All proof ingredients are already present: C0 (this ASN), reach definition and T1 (ASN-0034), well-formedness (this ASN), and B1/B2/M0 (ASN-0058). The review even supplies the complete proof sketch. This is a straightforward promotion from observation to lemma.

## Issue 3: C1a reconstruction verifies B3 but omits B1/B2
Category: INTERNAL
Reason: M7f is already established in ASN-0058 and covers exactly the needed frame property. The fix is either a citation of M7f or a one-line verification that V-extent union preserves coverage and disjointness — both derivable from existing definitions without external evidence.
