# Channel Assignment — ASN-0075 review-47

**Date:** 2026-06-03 08:33

## Issue 1: Observationality used before it is stated (defer-to-downstream)
Reason: This is a structural reordering — move the D-OBS observational claim before the wp analysis. The fix is purely internal: D-OBS is already stated in the note, only its position relative to the wp derivations needs changing. No design intent or implementation evidence is involved.

## Issue 2: Defensive "not an additional postcondition" meta-prose
Reason: The fix is a deletion of a defensive sentence that the wp formula already makes self-evident. Derivable from the ASN alone; no external channel needed.

## Issue 3: Independence-from-hypothesis aside in the disjointness argument
Reason: The fix drops a defensive clause and lets the existing contradictory `M(d_B)`-membership argument stand on its own. Purely internal prose tightening; no design or implementation question arises.
