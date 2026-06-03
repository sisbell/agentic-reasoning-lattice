# Channel Assignment — ASN-0091 review-38

**Date:** 2026-06-03 12:09

## Issue 1: S5 is discharged with a justification that does not justify it
Reason: The fix is internal — S5's status as a state-independent existential over the model class is given by its own foundation definition (already cited in the review), and the ASN supplies the template (RE-origin) for discharging state-independent results. No design intent or implementation evidence is needed; this is a restatement of why a known theorem holds.

## Issue 2: RA-adm's quantifier is ill-typed for non-per-state foundation results
Reason: The fix is internal — partitioning the foundation invariants into per-state predicates versus composite-boundary (P4★/P4a/P7a) and state-independent theorems (S5, T0(a/b)) is derivable from the foundation definitions and the ASN's own existing treatment (the dedicated P4a Handling and S5 discharges). Restating RA-adm to range over per-state invariants requires no external intent or code evidence.
