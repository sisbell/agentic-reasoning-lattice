# Channel Assignment — ASN-0043 review-55

**Date:** 2026-05-13 11:35

## Issue 1: L9 quantifier scope contradicts the proof's domain
Reason: The fix concerns formal precondition discipline — either restating L9 with an explicit `zeros(r) ≤ 2` antecedent or deriving that condition from T10a as already stated in ASN-0034. No design-intent or implementation evidence is needed; the gap is internal to the formal statement and references invariants already in the lattice.

## Issue 2: L1a uses home(a) and L1c before they exist
Reason: Pure presentation/ordering fix. Either reorder the definitions of `home(a)` and L1c before L1a, or restate L1a using the direct field-extraction formula. No external evidence needed.

## Issue 3: L6's formal statement is a definitional consequence of tuple typing
Reason: This is a formalization choice — recast L6 as a structural commitment on the `Link` type, or strengthen it to a positional-accessor predicate mirroring L5's set-semantics formulation. The substantive content (slots are first-class positions) is already cited from both Nelson and Gregory in the surrounding prose; the question is how to encode it formally.
