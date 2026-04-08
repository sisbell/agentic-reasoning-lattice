# Contract Review — ASN-0034 (cycle 2)

*2026-04-08 09:32*

### TA7a

The proof establishes a detailed case analysis for `⊖`'s S-membership behavior that the contract omits entirely, capturing only the single-component case.

- `MISSING_POSTCONDITION: For ⊖ with actionPoint(w) ≥ 2 and #w ≤ #o — the proof shows divergence falls at position 1 (where o₁ > 0 ≠ 0 = w₁), so TumblerSub produces o itself (a no-op), and the result lies in S. The contract says nothing about this case.`

- `MISSING_POSTCONDITION: For ⊖ with actionPoint(w) = 1 and divergence position d > 1 (i.e., o₁ = w₁ > 0) — the proof explicitly shows the result has r₁ = 0 and lies in T \ S, giving the counterexample [5,3] ⊖ [5,1] = [0,2]. The contract omits this negative result entirely.`

- `MISSING_POSTCONDITION: For ⊖ when #w > #o — the proof's "Preliminary" case states the result inherits trailing zeros at positions #o+1 through #w and lies in T \ S. The contract omits this case.`

1 mismatches.
