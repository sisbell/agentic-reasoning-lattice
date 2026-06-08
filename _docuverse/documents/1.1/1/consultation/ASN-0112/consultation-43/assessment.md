# Channel Assignment — ASN-0112 review-43

**Date:** 2026-06-08 12:08

## Issue 1: wp Tight re-derives V-ReachTight instead of citing it
Reason: Purely structural — replace the repeated D1/D0 walk with a one-line citation of the already-established V-ReachTight claim. No design intent or implementation fact is at stake; the fix is internal to the note's own proof structure.

## Issue 2: the `#origin_d > #reach_d` overshoot is established at five separate sites
Reason: Editorial consolidation — designate V2 case 2 as the canonical derivation and have the other four sites cite it. The fact is already proven internally; nothing external is needed to decide which site owns the proof.

## Issue 3: implementation remark offers "evidence" for an already-proven theorem
Reason: The fix is a reframing of how an already-proven invariant (V2 positivity, discharged by D0) relates to implementation behavior; the conformance direction is derivable from the ASN's own proof, requiring no new evidence from Gregory.
