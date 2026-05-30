# Channel Assignment — ASN-0042 review-113

**Date:** 2026-05-30 04:21

## Issue 1: The O1a/T4/O1b invariance induction is proved twice
Reason: Pure deduplication — both sites already exist in the ASN with identical induction skeletons sharing base case O14 and the O13/O15 steps. Consolidating to one derivation and citing it is fully internal.

## Issue 2: O7(c) hedges over future states the postcondition does not quantify over
Reason: The postcondition's scope (entry state Σ') and condition (v)'s next-reachability requirement are already in the ASN; deleting the out-of-scope Σ'' walkthrough and disclaimer requires no external input.

## Issue 3: O8 proof appends a case-walk the postcondition excludes
Reason: O8's postcondition (`ω ≠ π`) and its longest-match argument are self-contained in the ASN; removing the trailing "who the owner is" paragraph is a deletion derivable from the claim itself.

## Issue 4: `pfx` introduction pre-states and forward-references O1b, which then restates it
Reason: The redundant prose, the forward pointer, and the framing inconsistency (flat statement vs. derived invariant per the table/Delegation section) are all resolvable from the ASN's own existing treatment of O1b.

## Issue 5: `ω_Σ(a)` definition prose forward-points instead of advancing the definition
Reason: The signature `ω_Σ : Σ.B → Π_Σ` and the immediately-following O2 already carry the well-definedness; deleting the announcing sentences is internal.

## Issue 6: Field-decomposition reasoning re-derived inline in O9 (and elsewhere)
Reason: FieldStructure already establishes the separator-position and field-extraction facts within the ASN; replacing the repeated inline zero-scans with citations to it is fully internal.
