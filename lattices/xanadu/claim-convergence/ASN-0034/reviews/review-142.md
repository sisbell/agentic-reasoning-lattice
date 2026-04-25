# Cone Review — ASN-0034/T1 (cycle 5)

*2026-04-17 09:50*

Reviewing the current ASN content, checking for new issues not in previous findings.

### Case 3's reverse-witness rebuttals consume NAT-addcompat without citation

**Foundation**: NAT-addcompat (NatAdditionOrderCompatibility).

**ASN**: T1 (LexicographicOrder), part (b) Trichotomy, Case 3. The `m < n` branch states: *"No witness for `b < a` exists: case (i) would require `bⱼ < aⱼ` at some position `j ≤ min(m, n)`, but all such positions have equal components; case (ii) would require `b` to be a proper prefix of `a`, i.e., `n < m`, contradicting `m < n`."* The symmetric `n < m` branch runs the mirrored argument.

**Issue**: The "case (ii) would require `b` to be a proper prefix of `a`" step expands, per T1's definition of case (ii) applied to the reverse witness for `b < a`, to `k' = #b + 1 ≤ #a`, i.e., `n + 1 ≤ m`. The prose then rewrites this directly as "`n < m`" and contradicts `m < n` via NAT-order's trichotomy. Converting `n + 1 ≤ m` into `n < m` is the backward direction `n + 1 ≤ m ⟹ n < m`, which (per the cycle 4 finding for sub-case (ii, ii)) routes through NAT-addcompat's strict successor inequality `n < n + 1` composed with NAT-order's transitivity (strict disjunct) or substitution (equality disjunct) after unpacking `n + 1 ≤ m` via NAT-order's `≤` definition. The T1 Depends lists NAT-addcompat at six sites, none of which is Case 3's reverse-witness rebuttal. The symmetric `n < m` branch's case (ii) rebuttal for `a < b` — where `m + 1 ≤ n` is rewritten as `m < n` — has the same structure and is likewise absent from the enumeration. Under T0's citation convention ("each proof cites only the ℕ facts it actually uses"), the enumeration is an exhaustive list; Case 3's two branches contribute two missing NAT-addcompat sites.

**What needs resolving**: Either extend the NAT-addcompat enumeration to include Case 3's two reverse-witness rebuttals (`b < a` via case (ii) in the `m < n` branch and its mirror in the `n < m` branch), or restructure the rebuttal to route through an already-enumerated site — for instance, by deriving the contradiction directly from the conjunction `n + 1 ≤ m ∧ m < n` via NAT-order transitivity to `n + 1 < n`, then citing the `k' = k` / `k' < k` rebuttal machinery's existing NAT-addcompat site. The NAT-order trichotomy count may need parallel adjustment depending on which refutation route is chosen.
