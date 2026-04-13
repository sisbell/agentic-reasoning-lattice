# Contract Review — ASN-0036 (cycle 1)

*2026-04-12 19:50*

### S7

- `INACCURATE: Postcondition (d) states the decidability bound as "O(min(|a₁|, |a₂|)) component checks", but the comparison being described is of origin(a₁) vs origin(a₂) — document-level tumblers, which are strict prefixes of a₁ and a₂. The correct bound is O(min(|origin(a₁)|, |origin(a₂)|)). The proof itself states no complexity figure; the contract appears to have borrowed the O(min(|a₁|, |a₂|)) formula from S4's contract, where it describes comparison of full I-addresses. Using |a₁| and |a₂| here misrepresents both the objects being compared and the cost of comparing them.`

### V_S(d)

- `MISSING_POSTCONDITION`: The proof states "V_S(d) partitions dom(Σ.M(d)) by subspace identifier" — this is a substantive consequence of the definition and should appear as a postcondition, e.g., `(A S₁, S₂ : S₁ ≠ S₂ :: V_{S₁}(d) ∩ V_{S₂}(d) = ∅) ∧ ⋃_{S≥1} V_S(d) = dom(Σ.M(d))`.
- `MISSING_POSTCONDITION`: The proof states "Within V_S(d), all positions share a common depth by S8-depth" — this depth-uniformity property is established in the proof section but is absent from the contract entirely.

2 mismatches.
