# Revision Categorization — ASN-0036 review-61

**Date:** 2026-04-09 11:40



## Issue 1: S8 proof assumes m ≥ 2 via forward reference to ValidInsertionPosition
Category: INTERNAL
Reason: The fix is entirely derivable from existing definitions — the proof already identifies the m=1 case and sketches the resolution. The required change is restructuring the proof to handle m=1 directly using T3 and the singleton interval argument already present in the issue description, then removing the forward reference.

## Issue 2: Correspondence run definition uses ordinal displacement at k = 0, which is undefined
Category: INTERNAL
Reason: This is a notational gap in the ASN's own definitions. OrdinalShift's precondition (n ≥ 1) and the base case semantics (v + 0 = v) are both internal to ASN-0036 and ASN-0034. The fix is a convention extension or definition restructure — no external evidence needed.

## Issue 3: S8a status in Properties table misattributes logical dependency
Category: INTERNAL
Reason: The proof text within the ASN already states S8a is a design requirement, and the dependency on S7b is motivational not logical. The fix is correcting the Properties table to match the ASN's own proof — a purely editorial change requiring no external evidence.
