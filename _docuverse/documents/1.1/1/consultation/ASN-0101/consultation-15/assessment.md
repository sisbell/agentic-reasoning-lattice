# Channel Assignment — ASN-0101 review-15

**Date:** 2026-05-27 19:24

## Issue 1: Confusing partition phrasing in D8 Group (iii) P4★ argument
Reason: Pure prose clarification — the fix is to rephrase the partition expression so S' is unambiguously tied to its role as the complement of the affected subspace S. No design intent or implementation evidence required.

## Issue 2: Incorrect citation of TS2 in D1 proof
Reason: Internal proof correction — the conflation of functionality and injectivity is resolved by restructuring the argument (use TS2's contrapositive via T1 irreflexivity) or by citing OrdinalShift's definition for the functionality step. Both ASN-0034 properties referenced are already established.

## Issue 3: "Vacuously at length 1" misnomer in S8★ justification
Reason: Terminology fix — the quantifier range {0} is non-empty, so the discharge is trivial (via OrdinalShiftBase) not vacuous. Derivable from the ASN's own logic and the already-cited ASN-0034 base case.
