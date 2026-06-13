# Channel Assignment — ASN-0132 review-10

**Date:** 2026-06-13 08:28

## Issue 1: Revision scar and citation roadmap in CN-MONO
Reason: Pure deletion of editorial scar — the E-INV parenthetical footnotes a citation the proof does *not* use, and the "Each remaining fact is cited where it lives" filler announces structure. The proof's actual support (L12, LP13, CN-LOC, and the `L_R^{Σ'} = L_R^Σ` step) is already cited and present in the ASN, so removing the dead text needs nothing external.

## Issue 2: The resolution-boundary separation is stated three times
Reason: Deduplication and restructuring of a point already made — the general separation and both distinct applications (empty-request zero, re-phrasing-after-edit caveat) are all present in the ASN; the fix only consolidates them and strips back-pointers. No design intent or implementation evidence is at issue.

## Issue 3: Defensive framing of the `nullified` clause in CN-STAB
Reason: Prose tightening with the corrected phrasing supplied verbatim; the load-bearing content (`nullified` is selected from `L_R^Σ`, hence `Σ.L`-determined, hence `Σ'.L = Σ.L` discharges F-PRES) is correct and already in the ASN. The fix is purely internal restatement.
