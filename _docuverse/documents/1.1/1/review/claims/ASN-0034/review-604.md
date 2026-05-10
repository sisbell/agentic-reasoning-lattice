# Cone Review — ASN-0034/T10a (cycle 8)

*2026-04-26 05:27*

### NAT-order Depends entry omits case `k = 0` use sites
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder) — supplies transitivity `m < n ∧ n < p ⟹ m < p` and irreflexivity `¬(n < n)` (the latter via the `≠`-from-`<` step)
**ASN**: TA5a, Depends list, NAT-order entry: "at-least-one trichotomy ... splits `k ≥ 3` into the sub-branches `k = 3` and `3 < k` at case `k ≥ 3`; ... ; transitivity additionally chains `1 ≤ #t < #t + 1` (giving `1 ≤ #t + 1`) and `#t + 1 < #t + 2 ≤ #t + k = #t'` (giving `#t + 1 < #t'`) at case `k ≥ 3`." The proof prose for case `k = 0`: "by NAT-zero and NAT-addcompat, `t_{sig(t)} + 1 > t_{sig(t)} ≥ 0`, so `t_{sig(t)} + 1 ≠ 0`."
**Issue**: The NAT-order entry catalogs uses only at case `k ≥ 3`, but case `k = 0`'s NAT chain consumes NAT-order in two ways: (1) transitivity to chain `t_{sig(t)} + 1 > t_{sig(t)} ≥ 0` into `t_{sig(t)} + 1 > 0`; (2) the inference `> 0 ⟹ ≠ 0`, which routes through irreflexivity (or equivalently, the exactly-one trichotomy clause). The case `k = 0` chain is itself invoked at four sites within the case (T4(ii)'s `i = sig(t)` and `i + 1 = sig(t)` sub-branches, T4(iv)'s discharge, T4(iii)'s `sig(t) = 1` sub-case, and the zero-index set equality's primed exclusion at position `sig(t)`), so the NAT-order omission masks a structurally pervasive dependency. The prose attribution "by NAT-zero and NAT-addcompat" further reinforces the omission by naming only two of the three axioms the chain consumes. This parallels exactly the cycle 6 T0 use-site inventory gap, in which "case `k ≥ 3`" narrowed a surface used at multiple cases.
**What needs resolving**: Extend the NAT-order entry to include case `k = 0`'s use of transitivity (chaining `t_{sig(t)} + 1 > t_{sig(t)}` with `t_{sig(t)} ≥ 0` to obtain `t_{sig(t)} + 1 > 0`) and of irreflexivity (or asymmetry-of-`<`) to step from `> 0` to `≠ 0`. Optionally tighten the proof's prose attribution at the case `k = 0` NAT chain so the three axioms (NAT-zero, NAT-addcompat, NAT-order) are named at the point of consumption.

### NAT-closure Depends entry omits case `k ≥ 3` use sites
**Class**: REVISE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity) — closure of `+` on ℕ, ensuring sums of ℕ-elements re-enter ℕ
**ASN**: TA5a, Depends list, NAT-closure entry: "addition closure instantiated at `(t_{sig(t)}, 1)` with `1 ∈ ℕ` from the same axiom places `t_{sig(t)} + 1 ∈ ℕ` at case `k = 0`."
**Issue**: The entry attributes NAT-closure to case `k = 0` only, but case `k ≥ 3` uses NAT-closure repeatedly to close the sums it manipulates into ℕ — `#t + 1`, `#t + 2`, `#t + k`, `(#t + 1) + 1`, `1 + 1` — without which the cited NAT-addcompat strict-successor instantiations (`n < n + 1` at `n = #t`, `n = #t + 1`, `n = 2`) would be ill-typed (`n + 1` must lie in ℕ for the inequality to compare two ℕ-elements). NAT-addassoc's identification `(#t + 1) + 1 = #t + (1 + 1) = #t + 2` likewise needs all three terms in ℕ. The case `k ≥ 3` discharge of `1 ≤ #t + 1` chains through `#t < #t + 1` and the lower bound `1 ≤ #t`; this comparison is between ℕ-elements only because NAT-closure places `#t + 1 ∈ ℕ`. None of these case-`k ≥ 3` consumptions of closure are recorded, despite the entry's specificity at case `k = 0`. The omission parallels the cycle 6 T0 inventory gap.
**What needs resolving**: Extend the NAT-closure entry to enumerate the case `k ≥ 3` uses — closure of `#t + 1`, `#t + 2`, `#t + k` (and `(#t + 1) + 1`, `1 + 1` if the explicit identifications via NAT-addassoc are deemed worth itemising) into ℕ so the strict-successor and order-compatibility instantiations stay within signature.

VERDICT: REVISE
