# Revision Categorization — ASN-0057 review-1

**Date:** 2026-03-19 18:52

## Issue 1: D1 stated at #a = #b when the natural boundary is D0 + #a ≤ #b
Category: INTERNAL
Reason: The review identifies that the ASN's own analysis already contains all pieces needed for the generalization — the component-by-component proof, TumblerSub's length formula max(#a, #b), and the parenthetical's own observation about #a < #b. The fix requires only reorganizing and tightening reasoning already present in ASN-0057 and ASN-0034.

## Issue 2: No concrete example
Category: INTERNAL
Reason: Constructing a worked example requires only applying TumblerAdd, TumblerSub, and divergence — all defined in ASN-0034 — to specific tumbler values. The review even supplies candidate values. No design intent or implementation evidence is needed.

## Issue 3: Foundation name mismatch — "TumblerSubtract" for "TumblerSub"
Category: INTERNAL
Reason: Mechanical rename to match ASN-0034's established identifier. The correct name is already in the foundation; the fix is a string replacement.
