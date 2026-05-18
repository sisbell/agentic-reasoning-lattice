# Channel Assignment — ASN-0051 review-67

**Date:** 2026-05-17 19:12

## Issue 1: (m=1, p≥3) attainment not witnessed
Reason: The fix is derivable from the ASN's own block-decomposition machinery (C1a, S5) and span definitions. Either trimming the claim to match witnessed scope or constructing the witness uses only existing definitions; no design intent or implementation evidence is needed.

## Issue 2: SV13 synthesis scope under-specified
Reason: All four omitted properties (SV7/SV9/SV10/SV14) are already established in the ASN; the fix is editorial — either extending SV13 with a system-level clause or scoping SV13 as per-link with a pointer. No external input required.

## Issue 3: SV5 "multiset" wording
Reason: The fix is a pure terminology correction internal to the proof. S2 (ArrangementFunctionality) already establishes that M(d) is a function, so ran(M(d)) is a set; replacing "multiset" with "set" is mechanical.

## Issue 4: Worked Example "two-span variant" obscures the W(2,2) lift base
Reason: The fix is editorial cross-referencing between the Worked Example's two-span scenario and the W(m,p) lift family naming convention already established in SV11. No external input needed.
