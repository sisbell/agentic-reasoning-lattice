# Channel Assignment — ASN-0051 review-39

**Date:** 2026-05-16 02:53

## Issue 1: Notation note's description of shift conflicts with the OrdinalShift definition
Reason: The fix is a notation correction derivable from ASN-0034's OrdinalShift/TumblerAdd definitions already referenced in the ASN and the reviewer's identified replacement text. No design intent or implementation evidence is required — this is internal correction of a phrasing that contradicts a definition the ASN already cites.

## Issue 2: Apparent circularity in SV6's T4-validity verification of t
Reason: The fix is purely proof-structural — replacing a circular premise (`t₁ ≠ 0`) with the available precondition (s's T4-validity) that the reviewer has already identified. The reasoning lives entirely within the proof and SV6's stated preconditions, so the correction is derivable from the ASN alone.
