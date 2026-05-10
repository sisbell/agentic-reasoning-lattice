# Cone Review — ASN-0034/T1 (cycle 7)

*2026-04-17 10:12*

### Inconsistent Case 3 branch counting convention across NAT-* enumerations

**Foundation**: NAT-discrete (NatDiscreteness), NAT-addcompat (NatAdditionOrderCompatibility), NAT-order (NatStrictTotalOrder).

**ASN**: T1 (LexicographicOrder), Depends enumeration. Case 3 has two mirror branches (`m < n` and `n < m`), each of which instantiates NAT-discrete's forward direction (at `m→m+1≤n` vs `n→n+1≤m`) for its primary witness and, within each branch's reverse-witness rebuttal, instantiates NAT-addcompat's strict successor inequality (`n < n+1` vs `m < m+1`) and NAT-order's transitivity (composing `n < n+1 < m` vs `m < m+1 < n`).

The NAT-addcompat enumeration counts these branches separately: *"part (b) Trichotomy, Case 3's `m < n` branch reverse-witness rebuttal..."* and *"Case 3's `n < m` branch reverse-witness rebuttal..."* (sites 4 and 5 of eight). The NAT-order transitivity enumeration likewise counts them separately (sites 5 and 6 of six).

But the NAT-discrete enumeration packages both branches under a single site: *"part (b) Trichotomy, Case 3, uses the forward direction `m < n ⟹ m + 1 ≤ n` to pass from the case hypothesis `m < n` to `k = m + 1 ≤ n` — the successor-comparison step that underwrites... T1 case (ii)'s witness for `a < b` (the symmetric `m > n` branch of the same Case 3 uses the mirrored instance `n < m ⟹ n + 1 ≤ m` at the corresponding site)"* — the mirrored instance is acknowledged parenthetically but folded into "two distinct sites" rather than counted as a third.

**Issue**: The enumeration mixes two incompatible counting conventions. For NAT-addcompat and NAT-order-transitivity, Case 3's two branches are counted as separate sites because each branch instantiates the axiom at a different symbol (`n < n+1` vs `m < m+1`, and correspondingly distinct transitivity compositions). For NAT-discrete, the two branches likewise instantiate the forward direction at two distinct symbols (`m+1 ≤ n` vs `n+1 ≤ m`) — the same instance-distinctness that earned separate sites for addcompat — yet they are packaged as one. Under T0's citation convention that each proof cites only the ℕ facts it actually uses, the enumeration serves as an auditable inventory of axiom consumptions; inconsistent per-instance vs per-case-type counting across axioms makes the inventory uncheckable. A reader trying to verify the "two distinct sites" claim for NAT-discrete against the parallel "eight distinct sites" claim for NAT-addcompat cannot reconcile them without first deciding which convention applies — and the enumerations themselves do not declare the convention.

**What needs resolving**: Either count Case 3's two branches consistently as two sites across all three enumerations (promoting NAT-discrete to three sites: Case 3 `m<n`, Case 3 `n<m`, Case k₂<k₁ case-(ii)) or consistently as one site across all three (collapsing NAT-addcompat's sites 4 and 5 into one "Case 3 rebuttals" site and NAT-order-transitivity's sites 5 and 6 likewise, adjusting the totals to seven and five respectively). The choice must be uniform, and the enumeration should make the convention explicit so the site counts can be audited against the proof text.
