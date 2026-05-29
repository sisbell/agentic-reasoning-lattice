# Channel Assignment — ASN-0036 review-128

**Date:** 2026-05-28 23:08

## Issue 1: S7c Depends mismatch — unjustified TA7a citation
Reason: Internal. S7c is a pure design axiom (`#E(a) ≥ 2`); its actual dependencies are visible in the statement and contract. Reconciling the table against the contract — and judging that TA7a's ⊕/⊖ closure plays no role — is derivable from the ASN alone.

## Issue 2: S7a Depends mismatch
Reason: Internal. Whether S7a rests on S0 or S7b is settled by reading S7a's own statement and its identification argument within the ASN; no external intent or implementation evidence is required.

## Issue 3: Repeated T10a.4 "surrounding T4-validity" boilerplate
Reason: Internal. Editorial deduplication — state the T10a.4→T4b rationale once at S7b and trim later citations. No channel needed.

## Issue 4: Triple deferral to the same downstream location
Reason: Internal. Editorial cleanup — keep the S8 postcondition deferral, drop the two redundant forward pointers. Derivable from the ASN's own structure.

## Issue 5: Reviser-drift in S5 cross-document construction
Reason: Internal. The construction binds `i ∈ {1, …, N+1}`, so the `i = 0` analysis is self-evidently superfluous against the ASN's own witness range; removing it requires no external input.
