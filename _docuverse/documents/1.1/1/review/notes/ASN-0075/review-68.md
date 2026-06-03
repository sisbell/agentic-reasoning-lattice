# Review of ASN-0075

This is a strong, largely self-contained ASN. The core argument (D-DISCR / D-NEED — that `R` is load-bearing and `(C,L,E,M)` cannot discriminate DELETED from NEVER_INCLUDED) is well-constructed, the two-history construction checks out, and the worked example is consistent end-to-end. The proofs of D-WIT, D-EXH, and D-DISJ are complete and case-exhaustive. The findings below are limited to a naming inaccuracy and forward-reference friction.

## REVISE

### Issue 1: D-ORD named "Order Preservation" but preserves no order
**ASN-0075, "Order Preservation" section / claims table (D-ORD)**: "D-ORD — Order Preservation … Each output half is a finite subset of T, inheriting T1's total order" — and the body explicitly states "the V-position order in which a deleted address appeared … is not preserved by R … is not recoverable."
**Problem**: The claim asserts nothing is *preserved*. SHOWDELETIONS takes no input ordering to carry through; the output is simply a set that happens to be T1-orderable, and the section openly disclaims preservation of the only candidate input order (V-position order). The label "Order Preservation" matches the foundation's genuine order-*preservation* theorems (TA1, TS1, TA3) where an operation carries an ordering relation through — a precise reader will expect that shape and find the opposite. The name overpromises.
**Required**: Rename to reflect the actual content (e.g. "Order Availability" / "T1-Orderability of Output"), and state the claim as: output is a finite subset of `T`, hence linearly ordered by T1's restriction, with no separate ordering structure carried by the operation.

### Issue 2: wp/termination analysis depends on claims stated later
**ASN-0075, "The SHOWDELETIONS Operation" (wp discussion)**: "Because the operation writes no state component (D-OBS), wp computations for state-level predicates pass through unchanged…" and "Termination is grounded in finiteness, just as output finiteness is in D-ORD…"
**Problem**: The wp and termination reasoning leans on D-OBS (observationality) and D-ORD (finiteness), but both claims are introduced several sections later ("Order Preservation," "Observational Frame"). The general pass-through rule `wp(SHOWDELETIONS, P) = (precondition) ∧ P(Σ)` is *justified by* D-OBS, yet D-OBS is not yet available to the reader. This forces a forward skip to follow the argument — the reading-order friction this note's anti-bloat classifier targets.
**Required**: Either move the observationality (D-OBS) and finiteness (the part of D-ORD establishing finite output) results ahead of the wp/termination discussion, or have the wp section establish its own finiteness/no-write premises locally (C-fin, S8-fin, P7 are already cited inline) without deferring to not-yet-stated claims.

## OUT_OF_SCOPE

### Topic 1: Per-occurrence (V-position-level) deletion granularity
**Why out of scope**: The "Classification is at I-address-set granularity" paragraph correctly scopes this out as a Vstream concern. This is a statement of what the operation does not address (not meta-prose) and belongs to DELETE/REARRANGE mechanics, which the scope section excludes. No action needed.

### Topic 2: Multi-document generalization and witness structure
**Why out of scope**: Raised appropriately in Open Questions; binary-pair witness structure is the scope of this ASN, and the n-ary generalization is correctly deferred.

VERDICT: REVISE
