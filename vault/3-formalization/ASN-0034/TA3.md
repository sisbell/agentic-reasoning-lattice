**TA3 (OrderPreservationUnderSubtractionWeak).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`.

*Proof.* We must show that for all `a, b, w ∈ T` with `a < b`, `a ≥ w`, and `b ≥ w`, the inequality `a ⊖ w ≤ b ⊖ w` holds under T1.

By TA2, since `a ≥ w` and `b ≥ w`, both `a ⊖ w` and `b ⊖ w` are well-formed tumblers in `T`, so the comparison is well-defined. We recall the subtraction rule (TumblerSub) for self-containment: given `x ≥ w`, zero-pad both operands to length `max(#x, #w)` and scan for the first position at which the padded sequences disagree. If no such position exists (we say `x` is *zero-padded-equal* to `w`), then `x ⊖ w` is the zero tumbler of that length. Otherwise, let `d` be the first divergence position; then `(x ⊖ w)ᵢ = 0` for `i < d`, `(x ⊖ w)_d = x_d - w_d`, and `(x ⊖ w)ᵢ = xᵢ` for `i > d` (all under zero-padding), with result length `max(#x, #w)`.

Since `a < b`, T1 provides two cases: either (i) there exists a first position `j ≤ min(#a, #b)` where `aⱼ < bⱼ`, or (ii) `a` is a proper prefix of `b` — `#a < #b` and `aᵢ = bᵢ` for all `i ≤ #a`. We treat each in turn, partitioning further by the divergence structure of the operands against `w`.

**Case A: `a` is a proper prefix of `b`** (T1 case (ii)). Then `#a < #b` and `aᵢ = bᵢ` for all `i ≤ #a`.

*Sub-case A1: `a = w`.* The subtraction `a ⊖ w` yields the zero tumbler of length `max(#a, #w) = #a`, since the operands are identical. Since `a` is a proper prefix of `b` and `a = w`, we have `bᵢ = wᵢ` for all `i ≤ #w = #a`. If some component `bᵢ` with `i > #w` is nonzero, the pair `(b, w)` has a divergence beyond `#w`, making `b ⊖ w` a positive tumbler; by TA6 the zero tumbler `a ⊖ w` is strictly less. If `bᵢ = 0` for all `i > #w`, the zero-padded sequences of `b` and `w` agree everywhere, so `b ⊖ w` is the zero tumbler of length `max(#b, #w) = #b`. Both results are zero tumblers, but `#(a ⊖ w) = #a < #b = #(b ⊖ w)`, so `a ⊖ w` is a proper prefix of `b ⊖ w`, giving `a ⊖ w < b ⊖ w` by T1 case (ii).

*Sub-case A2: `a > w` with divergence.* Let `dₐ` be the first position where the zero-padded sequences of `a` and `w` disagree. We claim `dₐ ≤ #a`: if `a > w` by T1 case (i), `dₐ ≤ min(#a, #w) ≤ #a`; if by T1 case (ii), `w` is a proper prefix of `a` and `dₐ` is the first `i > #w` with `aᵢ > 0`, so `dₐ ≤ #a`. Since `bᵢ = aᵢ` for all `i ≤ #a` and `dₐ ≤ #a`, the comparison of `b` against `w` (under zero-padding) agrees with that of `a` at all positions up through `dₐ`. So `d_b = dₐ = d`.

Apply TumblerSub to both. At positions `i < d`: both results are zero. At position `d`: both compute `a_d - w_d = b_d - w_d`, since `a_d = b_d` for `d ≤ #a`. At positions `d < i ≤ #a`: both copy from their respective minuends, giving `aᵢ = bᵢ`. The two results agree on positions `1, ..., #a`.

Beyond position `#a`, the results may differ. The result `a ⊖ w` has length `max(#a, #w)`, and `b ⊖ w` has length `max(#b, #w) ≥ max(#a, #w)` since `#b > #a`. At positions `#a < i ≤ max(#a, #w)` (present only when `#w > #a`): `(a ⊖ w)ᵢ = 0` from `a`'s zero-padding, while `(b ⊖ w)ᵢ = bᵢ` if `i ≤ #b` (copied from the minuend since `i > d`) and `0` if `i > #b` (from `b`'s zero-padding); in either case `(a ⊖ w)ᵢ ≤ (b ⊖ w)ᵢ`. If no disagreement exists on positions `1, ..., max(#a, #w)`, then `a ⊖ w` is a prefix of `b ⊖ w`, giving `a ⊖ w ≤ b ⊖ w` by T1 case (ii). If a first disagreement exists at position `p > #a`, then `(a ⊖ w)_p = 0 ≤ (b ⊖ w)_p`; if strict, `a ⊖ w < b ⊖ w` by T1 case (i); if `(b ⊖ w)_p = 0` at all such positions, then `a ⊖ w` is a prefix of `b ⊖ w`, giving `a ⊖ w ≤ b ⊖ w` by T1 case (ii).

*Sub-case A3: `a > w` without divergence (zero-padded equality).* Since `a > w` requires a structural difference yet the padded sequences agree everywhere, the only possibility is T1 case (ii): `w` is a proper prefix of `a` with `aᵢ = 0` for all `i > #w`. The subtraction `a ⊖ w` yields the zero tumbler of length `#a`. Since `b > a > w` and `#b > #a ≥ #w`, `b` agrees with `w` (hence with `a`) on positions `1, ..., #a`. The result `b ⊖ w` has length `max(#b, #w) = #b > #a`. If `b ⊖ w` has any positive component, then `a ⊖ w` (all zeros) is strictly less by TA6. If `b ⊖ w` is also a zero tumbler, `#(b ⊖ w) = #b > #a = #(a ⊖ w)`, so the shorter is a proper prefix of the longer, giving `a ⊖ w < b ⊖ w` by T1 case (ii).

In all sub-cases of Case A, `a ⊖ w ≤ b ⊖ w`.

**Case B: Component divergence at `j`** (T1 case (i)). There exists a first position `j ≤ min(#a, #b)` with `aⱼ < bⱼ` and `aᵢ = bᵢ` for all `i < j`.

*Sub-case B1: `a` is zero-padded-equal to `w`.* The subtraction `a ⊖ w` is the zero tumbler of length `max(#a, #w)`. At position `j`, zero-padded equality gives `wⱼ = aⱼ`, so `bⱼ > aⱼ = wⱼ`. The pair `(b, w)` diverges at or before `j`, making `b ⊖ w` positive. By TA6, `a ⊖ w < b ⊖ w`.

For the remaining sub-cases, `a` is not zero-padded-equal to `w`, so `dₐ = divergence(a, w)` is well-defined. The divergence `d_b = divergence(b, w)` is also well-defined: if `b` were zero-padded-equal to `w`, then at position `dₐ` we would have `a_{dₐ} > w_{dₐ} = b_{dₐ}` (from `a ≥ w` at the divergence), while `aᵢ = wᵢ = bᵢ` for all `i < dₐ` — making `dₐ` a position where `a > b`, contradicting `a < b`. Let `j` be the first position where `aⱼ < bⱼ`.

*Sub-case B2: `dₐ = d_b = d`.* Both operands diverge from `w` at the same position. For `i < d`, both results are zero. Since `a` and `b` agree with `w` before `d`, and `aⱼ < bⱼ`, we have `j ≥ d`. If `j = d`: `a_d - w_d < b_d - w_d` since `a_d < b_d`, so `a ⊖ w < b ⊖ w` by T1 case (i). If `j > d`: `a_d = b_d` (since the first `a`-vs-`b` disagreement is at `j > d`), so both results agree at position `d`; at positions `d < i < j`, both copy from their minuends which agree (`aᵢ = bᵢ`); at position `j`, `(a ⊖ w)ⱼ = aⱼ < bⱼ = (b ⊖ w)ⱼ` since both are in the tail-copy phase (`j > d`). By T1 case (i), `a ⊖ w < b ⊖ w`.

*Sub-case B3: `dₐ < d_b`.* At position `dₐ`, `a_{dₐ} ≠ w_{dₐ}` but `b_{dₐ} = w_{dₐ}`. Since both `a` and `b` agree with `w` at all positions before `dₐ`, the first disagreement between `a` and `b` is at `dₐ`, giving `j = dₐ` with `a_{dₐ} < b_{dₐ} = w_{dₐ}`. But `a ≥ w` requires `a_{dₐ} ≥ w_{dₐ}` at the divergence — contradiction. This case is impossible under the preconditions.

*Sub-case B4: `dₐ > d_b`.* At position `d_b`, `b_{d_b} ≠ w_{d_b}` but `a_{d_b} = w_{d_b}`. Since both `a` and `b` agree with `w` before `d_b`, the first disagreement between `a` and `b` is at `d_b`, giving `j = d_b` with `a_{d_b} = w_{d_b} < b_{d_b}` — the inequality holds because `b ≥ w` forces `b_{d_b} > w_{d_b}` at this divergence. The result `(a ⊖ w)_{d_b} = 0` since `d_b < dₐ` falls in the pre-divergence zero phase for `a ⊖ w`. The result `(b ⊖ w)_{d_b} = b_{d_b} - w_{d_b} > 0`. At all positions `i < d_b`, both results are zero. By T1 case (i), `a ⊖ w < b ⊖ w`.

In every case, `a ⊖ w ≤ b ⊖ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
- *Postconditions:* a ⊖ w ≤ b ⊖ w
