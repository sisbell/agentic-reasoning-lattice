# Cone Review — ASN-0034/T1 (cycle 8)

*2026-04-17 12:03*

### Uncounted NAT-order consumption at the divergence-set construction and Case 1's `m = n` derivation

**Foundation**: NAT-order (NatStrictTotalOrder).

**ASN**: T1 (LexicographicOrder), part (b) Trichotomy. The "first divergence position" construction appears in the main proof text ("Define the *first divergence position* `k` as the least positive integer... either because `aₖ ≠ bₖ` at some position present in both tumblers (`k ≤ m ∧ k ≤ n`), or because one tumbler is exhausted at position `k` while the other continues (`k = m + 1 ≤ n`, or `k = n + 1 ≤ m`)"), and the Depends enumeration formalises the set as `{i ∈ ℕ : 1 ≤ i ∧ i ≤ m ∧ i ≤ n ∧ aᵢ ≠ bᵢ} ∪ ({m + 1} when m < n, {n + 1} when n < m, else ∅)`. Case 1 then opens: *"no divergence exists. Then `m = n` and `aᵢ = bᵢ` for all `1 ≤ i ≤ m`, so `a = b` by T3."*

**Issue**: The set construction's three-way branch (`when m < n` / `when n < m` / `else`) is a NAT-order trichotomy invocation at the length pair `(m, n)` — the same axiom clause that Case 3's opening invokes at the same pair. It occurs *before* the case split into Case 1/2/3, in the shared machinery that underwrites the well-ordering appeal. Case 1's passage from "no divergence exists" to `m = n` is a second consumption at the same pair: unpacking "no divergence" forces `¬(m + 1 ≤ n) ∧ ¬(n + 1 ≤ m)`, from which `m = n` follows only via NAT-order trichotomy (ruling out both strict alternatives). Neither consumption appears in the thirteen-site trichotomy itemization, nor is either explicitly folded into Case 3's opening invocation under the co-pair absorption convention the enumeration elsewhere declares. The convention's footing requires the absorption to be stated when invoked (Case 3's opening site makes its three-way fold explicit; sub-case (ii, ii) and Case `k₂ < k₁` under case-(ii) of `b < c` are acknowledged in Previous Findings as sites where no prior invocation exists to absorb into). The divergence-set and Case 1 consumptions occur *before* Case 3's opening in the narrative, so Case 3's opening cannot be the "opening" invocation they reuse — whichever use is chronologically first at the length pair is the opening, and the Case 3 site description would then need restating as a co-pair reuse rather than the opener.

**What needs resolving**: Either enumerate the divergence-set construction's trichotomy use and Case 1's trichotomy use as additional NAT-order sites (raising the trichotomy count and the preamble total, with per-instance counting decisions matching the Case 2/Case 3 conventions already applied), or declare them as co-pair reuses of a single opening invocation at `(m, n)` — with the Case 3 opening site's description rewritten to reflect that it is the downstream reuse rather than the opener, and with the trichotomy consumptions at the divergence-set step and Case 1 explicitly cited as folding into that opening. The enumeration must either count every NAT-order consumption or declare the absorption path for each reuse; at present these two pre-case consumptions fall outside both routes.

## Result

Cone not converged after 8 cycles.

*Elapsed: 4984s*
