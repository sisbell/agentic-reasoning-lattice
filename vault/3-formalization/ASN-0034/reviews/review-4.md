# Contract Review — ASN-0034 (cycle 1)

*2026-04-08 09:29*

### TA7a

- `INACCURACY: For ⊖, the proof's own formal TA7a statement quantifies over w > 0: "(A o ∈ S, w > 0 : o ≥ w ⟹ o ⊖ w ∈ T)". The contract's preconditions for ⊖ list only "o ∈ S, w ∈ T, o ≥ w" — dropping w > 0. The contract is weaker-preconditioned than what the proof claims to establish for ⊖, creating an asymmetry with the ⊕ preconditions where w > 0 is correctly retained.`

- `MISSING_POSTCONDITION: The proof establishes a concrete S-membership result for ⊖ on single-component ordinals: "[x] ⊖ [n] is [x − n] ∈ S when x > n, or [0] ∈ Z when x = n (a sentinel, TA6)" — i.e., for single-component ordinals, ⊖ gives closure in S ∪ Z. The contract includes an analogous S-membership condition for ⊕ ("the result is in S when all tail components of w after the action point are positive") but is entirely silent on the corresponding analysis for ⊖, leaving the proven single-component S ∪ Z closure result uncaptured.`

1 mismatches.
