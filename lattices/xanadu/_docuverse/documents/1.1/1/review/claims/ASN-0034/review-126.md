# Cone Review — ASN-0034/Span (cycle 3)

*2026-04-17 04:09*

Reviewing the ASN as a system for new cross-cutting issues not already flagged in previous cycles.

### T1's NAT-discrete citation omits Case `k₂ < k₁`'s derivation of `k₂ ≤ m` under the case-(ii) branch of `a < b`
**Foundation**: (foundation ASN — internal consistency; per-step NAT-* citation convention)
**ASN**: T1's proof, part (c) Transitivity, Case `k₂ < k₁`, reads: *"Therefore `b < c` is via case (i): `bₖ₂ < cₖ₂` with `k₂ ≤ min(n, p)`. Since `k₂ < k₁` and `a` has components at all positions below `k₁`, we have `k₂ ≤ m`, giving `aₖ₂ = bₖ₂ < cₖ₂` with `k₂ ≤ min(m, p)`."* The hypothesis splits on how `a < b` was witnessed. In the case-(i) branch, `k₁ ≤ min(m, n) ≤ m`, so `k₂ < k₁ ≤ m` yields `k₂ ≤ m` by NAT-order alone. In the case-(ii) branch, however, `k₁ = m + 1`, and the passage `k₂ < k₁ = m + 1 ⟹ k₂ ≤ m` invokes NAT-discrete's no-natural-between-`m`-and-`m+1` axiom (the form `n < m + 1 ⟹ n ≤ m`, equivalent to the backward direction `m + 1 ≤ n ⟺ m < n` rewritten at the contrary). T1's current NAT-discrete annotation enumerates exactly two sites: *"part (b) Trichotomy, Case 3, uses the forward direction `m < n ⟹ m + 1 ≤ n`"* and *"part (c) Transitivity, sub-case (ii, ii), uses the backward direction `m + 1 ≤ n ⟹ m < n`."* The present site — part (c), Case `k₂ < k₁`, under the case-(ii) branch of `a < b` — is not acknowledged.
**Issue**: The ASN's per-step citation convention, applied with full granularity elsewhere in T1 (NAT-addcompat at two sites, NAT-order at four sites, NAT-cancel at one, NAT-wellorder at one), leaves this NAT-discrete site tacit. The `k₂ ≤ m` conclusion is load-bearing for the argument: the T1 case (i) witness for `a < c` in Case `k₂ < k₁` requires `k₂ ≤ min(m, p)`, and without `k₂ ≤ m` the witness has no bound on `m`. The narrative's phrase "a has components at all positions below k₁" smooths over the discreteness appeal — when `k₁ = m + 1`, translating "positions below `k₁`" to the set `{1, ..., m}` is exactly the no-gap-between-`m`-and-`m+1` axiom. A reviser tightening or re-stating NAT-discrete has Depends-backed visibility only into the Case 3 and sub-case (ii, ii) sites and would miss Case `k₂ < k₁`'s branch-(ii) dependence on the same axiom.
**What needs resolving**: T1's NAT-discrete annotation must enumerate the part (c) Case `k₂ < k₁` site under the case-(ii) branch of `a < b` alongside the two existing sites, matching the granularity the same Depends applies to NAT-order and NAT-addcompat; alternatively, the proof must restructure Case `k₂ < k₁` so that it does not pass through `k₂ < m + 1 ⟹ k₂ ≤ m` in the case-(ii) branch — for instance, by deriving `k₂ ≤ m` uniformly in both branches through a cited argument that makes the discreteness use visible.

## Result

Cone not converged after 3 cycles.

*Elapsed: 1457s*
