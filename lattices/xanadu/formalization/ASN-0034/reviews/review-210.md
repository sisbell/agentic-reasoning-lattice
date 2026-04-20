# Cone Review — ASN-0034/TA-assoc (cycle 6)

*2026-04-17 23:23*

### TA-assoc's existential witness for `Pos(s)` elides index-bound validity

**Foundation**: TA-Pos (PositiveTumbler, this ASN) — defining existential `Pos(w) ⟺ (E i : 1 ≤ i ≤ #w : wᵢ ≠ 0)`; ActionPoint (this ASN) — supplies `1 ≤ k_b ≤ #b` and `1 ≤ k_c ≤ #c`; TA0 (this ASN) — supplies `#s = #(b ⊕ c) = #c`.

**ASN**: TA-assoc (AdditionAssociative), *Action point of `s`*: "In every sub-case `s` has a nonzero component at position `min(k_b, k_c)`, and this nonzero component witnesses TA-Pos's defining existential `(E i : 1 ≤ i ≤ #s : sᵢ ≠ 0)` at `i = min(k_b, k_c)` — thereby establishing `Pos(s)`". The Depends clause for TA-Pos repeats the same claim verbatim.

**Issue**: Witnessing the existential at `i = min(k_b, k_c)` requires `1 ≤ min(k_b, k_c) ≤ #s`. The proof exhibits the nonzero component in each sub-case but does not discharge either bound. The lower bound `1 ≤ min(k_b, k_c)` chains through ActionPoint's `1 ≤ k_b` and `1 ≤ k_c` via a property of `min` over ℕ (`min(x, y) ≥ 1` when `x ≥ 1` and `y ≥ 1`). The upper bound `min(k_b, k_c) ≤ #s = #c` chains through `min(k_b, k_c) ≤ k_c` (a property of `min`) composed with ActionPoint's `k_c ≤ #c` and TA0's `#s = #c`. Both properties of `min` are used silently (also in *Domain conditions*, where `k_b ≤ #a ⟹ min(k_b, k_c) ≤ #a` depends on `min(k_b, k_c) ≤ k_b`), yet `min` is neither in T0's NAT-* enumeration nor given a defining clause in this ASN. Per-step citation discipline elsewhere (TumblerAdd's dominance proof, ActionPoint's bound usages) carefully sources every `≤` step on ℕ; the witness step here does not.

**What needs resolving**: Either establish `1 ≤ min(k_b, k_c) ≤ #s` as explicit sub-steps with citations (ActionPoint on both `b` and `c` for the lower bound; ActionPoint on `c` plus a sourced `min(x, y) ≤ y` for the upper bound; TA0 for `#s = #c`), or introduce `min` as a named definition over ℕ with its monotonicity properties derived from NAT-order so that subsequent invocations — here and in *Domain conditions* — have a licensed source.
