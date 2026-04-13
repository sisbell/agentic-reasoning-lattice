# Contract Review — ASN-0036 (cycle 1)

*2026-04-13 14:11*

### S7

`

- `MISSING_PRECONDITION: T3 (CanonicalRepresentation, ASN-0034) is cited in the proof's uniqueness section — "By T3 (CanonicalRepresentation, ASN-0034), this distinctness is decidable by component-wise comparison" — as a logical step supporting the decidability of origin inequality. Following the project convention of listing theorem dependencies as preconditions (S0, S4, S7a, S7b, T4, and GlobalUniqueness are all listed this way), T3 should appear in the precondition list but does not.`

### S8-depth

- `MISSING_POSTCONDITION`: The proof explicitly establishes subspace preservation for V-positions within a run — `(A k : 0 ≤ k < n : (v+k)₁ = v₁)` — via TumblerAdd's prefix rule (the subspace identifier component is before the action point and is copied unchanged). The contract omits this.

- `MISSING_POSTCONDITION`: The proof explicitly establishes subspace preservation for I-addresses within a run — the element subspace identifier E₁ of `a+k` equals E₁ of `a` for all k — as a combined result of S7c (element-field depth δ ≥ 2 places E₁ outside the action point) and TumblerAdd's prefix rule. The contract omits this.

- `MISSING_POSTCONDITION`: The proof explicitly states that `a+k` produces a result of length `#a` ("TumblerAdd's prefix rule copies all earlier components … unchanged, producing a result of length `#a`"). The contract does not capture `#(a+k) = #a`.

### S9

`

- `MISSING_PRECONDITION: S0 (content immutability) — the proof's sole inference engine is S0's unconditional guarantee. The contract lists no preconditions at all. The Frame entry mentions S0 parenthetically, but a Frame clause describes what is preserved, not what is assumed. By direct analogy with S3's contract, which explicitly lists "S1 (store monotonicity)" as a precondition, S9's contract should list "S0 (content immutability)" as a precondition.`

3 mismatches.
