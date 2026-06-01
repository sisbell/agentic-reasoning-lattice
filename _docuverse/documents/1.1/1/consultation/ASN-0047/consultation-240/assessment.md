# Channel Assignment — ASN-0047 review-240

**Date:** 2026-06-01 11:38

## Issue 1: "Link store and extended system state" is a near-empty structural slot holding only deferral prose
Reason: This is an editorial deletion/fold decision — the link store is already defined in *The state model*, L3 already carries `e₃ ≠ ∅`, and the deferral duplicates an existing Open Question. The fix is fully derivable from the ASN's own structure.

## Issue 2: Redundant link-withdrawal / fork-inheritance deferrals duplicate Open-Question content in body prose
Reason: This is an internal redundancy removal — both inline sentences restate deferrals already present verbatim in the Open Questions, and removing them requires only confirming the duplication within the ASN. No design intent or implementation evidence is needed.
