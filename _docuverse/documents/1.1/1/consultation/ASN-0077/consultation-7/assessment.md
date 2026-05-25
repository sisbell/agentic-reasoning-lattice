# Channel Assignment — ASN-0077 review-7

**Date:** 2026-05-25 16:51

## Issue 1: O0(b) derivation conflates L1c and K.λ roles
Reason: Pure expositional restructuring — both L1c and K.λ are already cited foundation axioms from ASN-0047. The fix is to reorder the prose so L1c carries the structural identity and K.λ carries the allocator identity, with explicit composition. No external information needed.

## Issue 2: Vacuous "or ∅ otherwise" in V-span over link subspace
Reason: Internal consistency fix — precondition (vi) is already in the operation specification, and the ASN itself derives non-emptiness later. Either drop the branch or mark it vacuous. No external information needed.

## Issue 3: Singleton I-span proof relies on an implicit "no children of A_C(d)" reading without citing K.α
Reason: K.α's "Subsequent emission" rule is a foundation axiom in ASN-0047 already used elsewhere in this ASN. The fix is to insert a citation to K.α's `inc(max, 0)` algorithm at the load-bearing step. Foundation citation is internally available.

## Issue 4: O0(c) totality clause is stated but its load-bearing portion is forward-deferred
Reason: Pure organizational fix — either inline the one-step permanence argument (using O3 + P3, both already established) or drop the sub-clause and let O5 carry it. No external information needed.
