# Cone Review — ASN-0034/T2 (cycle 3)

*2026-04-17 13:14*

### T2 Depends omits NAT-wellorder
**Foundation**: NAT-wellorder (NatWellOrdering) — every nonempty subset of ℕ has a least element.
**ASN**: T2 proof, Case 1: "The scan finds `aₖ ≠ bₖ` after verifying `aᵢ = bᵢ` for all `1 ≤ i < k`. Exactly `k` component pairs are examined." T2 Formal Contract postcondition (b): "The number of component pairs examined is at most `#a` and at most `#b`." T2 Depends lists T0, T1, T3, NAT-order.
**Issue**: The count "exactly `k` component pairs examined" in Case 1 requires `k` to be the *first* divergence position — the scan stops at the least `i` with `aᵢ ≠ bᵢ`. Without well-ordering of ℕ, the scan could in principle encounter a divergence at some `k` while a strictly smaller divergence exists earlier, contradicting the agreement premise `aᵢ = bᵢ` for all `1 ≤ i < k` and breaking the bound. T1's proof discharges the analogous "first divergence position" claim from NAT-wellorder explicitly, but T2's Depends and narrative never invoke it, even though the same least-element reasoning underwrites T2's count.
**What needs resolving**: T2 must either add NAT-wellorder to its Depends list with Case 1's first-divergence site called out, or rework Case 1's count so that it does not rely on `k` being the least divergence position.

### T2 Depends narrative for NAT-order enumerates trichotomy only, omits transitivity
**Foundation**: NAT-order (NatStrictTotalOrder) — transitivity: `m < n ∧ n < p ⟹ m < p` and the derivable mixed form `i ≤ m ∧ m < n ⟹ i ≤ n`.
**ASN**: T2 proof, Case 2 sub-case `m < n`: "The shared range is exactly `{i : 1 ≤ i ≤ m}` — every position of `a`, each of which satisfies `i ≤ n` via the case hypothesis". T2 Depends narrative for NAT-order: "the proof invokes trichotomy on ℕ at two distinct sites" (only trichotomy sites enumerated).
**Issue**: Passing from `i ≤ m` and the case hypothesis `m < n` to `i ≤ n` is NAT-order transitivity (strict-and-nonstrict composition), not trichotomy. The symmetric sub-case `n < m` invokes the mirrored instance. T2's Depends lists NAT-order but its itemised narrative accounts only for two trichotomy sites (component pair and length pair), leaving these transitivity uses undocumented — a gap under the same per-site accounting discipline T1's Depends adopts.
**What needs resolving**: T2's NAT-order entry must either extend its site enumeration to cover the transitivity invocations in Case 2's `m < n` and `n < m` sub-cases, or rework those sub-cases so that `i ≤ n` (respectively `i ≤ m`) is obtained without composing across `<`.

## Result

Cone converged after 4 cycles.

*Elapsed: 2471s*
