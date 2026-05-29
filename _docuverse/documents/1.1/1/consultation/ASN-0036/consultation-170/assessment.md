# Channel Assignment — ASN-0036 review-170

**Date:** 2026-05-29 05:14

## Issue 1: Duplicated transition-invariant justification in the S5 proof
Reason: Pure editorial restructuring — hoist the transition-invariant observation above both constructions and delete the repeated "as above" sentence. No design intent or implementation evidence is at stake; the fix is mechanical and derivable from the proof's own structure.

## Issue 2: `shift(·, 0) = identity` extends a foundation operation by local fiat without stating the consistency obligation
Reason: The fix is internal — D-MIN already establishes `min(V_1(d)) = [1,…,1]`, so the `j = 0` case can be written explicitly as `v = min(V_1(d))` without extending OrdinalShift. Everything needed is present in the ASN's own content.

## Issue 3: Essay elaboration in a structural reasoning slot (S2)
Reason: Compressing or relocating interpretive commentary on a Nelson phrase is an organizational decision within the note; no new design intent or code evidence is required. The "heterogeneous origins" observation and its load-bearing home (S5) are both already in the ASN.
