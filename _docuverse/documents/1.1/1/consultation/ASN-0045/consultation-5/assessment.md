# Channel Assignment — ASN-0045 review-5

**Date:** 2026-05-13 22:17

## Issue 1: At-most-one step cites T4c's disjointness without bridging from label predicates to zeros equalities
Reason: The fix restructures the derivation using facts already cited in the ASN (T4c's Injectivity, NAT-card single-valuedness of zeros, substitutivity of `=`). No new design intent or implementation evidence is needed; both proposed paths (a) and (b) draw entirely on existing dependencies.

## Issue 2: Account rename equivalence asserted without derivation
Reason: The fix is to expose the biconditional chain through T4c's already-established `(zeros(t) = 1 ↔ t is a user address)` postcondition. The rename's sourcing from Nelson and Gregory is already documented in the Naming Convention; the derivation itself is internal logic.

## Issue 3: Numeral constants 2 and 3 misattributed in Depends
Reason: Pure attribution correction — reassigning 2 and 3 from NAT-closure to T4's *Numerals* sub-clause. Both dependencies are already in scope; no external consultation needed.
