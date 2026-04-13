# Contract Review — ASN-0036 (cycle 2)

*2026-04-12 19:53*

### S7

- `EXTRA_PRECONDITION: T10a is listed as a direct precondition but the S7 proof does not invoke it directly — it is a transitive dependency of GlobalUniqueness and S4, both used as black-box results. The proof's direct assumptions are S7b, T4, S7a, GlobalUniqueness, T3, S0, and S4.`
- `EXTRA_POSTCONDITION: Postcondition (d) adds "O(min(|origin(a₁)|, |origin(a₂)|)) component checks" but the S7 proof establishes only that distinctness is decidable by component-wise comparison (by T3) — no complexity bound is stated or derived in the S7 proof body.`

1 mismatches.
