**TA3 (OrderPreservationUnderSubtractionWeak).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`.

*Proof.* We show that for all `a, b, w ∈ T` with `a < b`, `a ≥ w`, `b ≥ w`, we have `a ⊖ w ≤ b ⊖ w`.

By TA2, `a ⊖ w` and `b ⊖ w` are well-formed tumblers in `T`. Recall TumblerSub: given `x ≥ w`, zero-pad both operands to `L_{x,w}` (the longer of `#x`, `#w`, dispatched by NAT-order's trichotomy on `(#x, #w)`) and scan for the first disagreement. If none exists, `x ⊖ w` is the zero tumbler of length `L_{x,w}`. Otherwise, let `d` be the first divergence; then `(x ⊖ w)ᵢ = 0` for `i < d`, `(x ⊖ w)_d = x_d - w_d`, and `(x ⊖ w)ᵢ = xᵢ` for `i > d`, with result length `L_{x,w}`.

Since `a < b`, T1 provides two cases: (i) there exists a first position `j` with `j ≤ #a ∧ j ≤ #b` where `aⱼ < bⱼ`, or (ii) `a` is a proper prefix of `b`.

**Case A: `a` is a proper prefix of `b`** (T1 case (ii)). Then `#a < #b` and `aᵢ = bᵢ` for all `i ≤ #a`.

*Sub-case A1: `a = w`.* NAT-order's trichotomy on `(#a, #w)` gives `L_{a,w} = #a`; `a ⊖ w` is the zero tumbler of that length. Since `a` is a proper prefix of `b` and `a = w`, `bᵢ = wᵢ` for all `i ≤ #w = #a`. If some `bᵢ` with `i > #w` is nonzero, `(b, w)` diverges beyond `#w`, making `b ⊖ w` positive; by TA6, `a ⊖ w < b ⊖ w`. Otherwise, the zero-padded sequences of `b` and `w` agree everywhere, and under `#w = #a < #b` NAT-order places `(#b, #w)` in sub-case (γ), giving `L_{b,w} = #b`; `b ⊖ w` is the zero tumbler of length `#b`. Both results are zero, agreeing on positions `1, ..., #a`; the strict length inequality `#a < #b` is converted by NAT-discrete into `#a + 1 ≤ #b` (with `#a + 1 ∈ ℕ` by NAT-closure), supplying T1 case (ii)'s witness. Thus `a ⊖ w < b ⊖ w` by T1 case (ii).

*Sub-case A2: `a > w` with divergence.* Let `dₐ` be the first position where the zero-padded sequences of `a` and `w` disagree. We claim `dₐ ≤ #a`: if `a > w` by T1 case (i), it supplies `dₐ ≤ #a ∧ dₐ ≤ #w`; if by T1 case (ii), `w` is a proper prefix of `a` and `dₐ` is the first `i > #w` with `aᵢ > 0`, so `dₐ ≤ #a`. Since `bᵢ = aᵢ` for all `i ≤ #a` and `dₐ ≤ #a`, `d_b = dₐ = d`.

At positions `i < d`: both results are zero. At position `d`: both compute `a_d - w_d = b_d - w_d`, each in ℕ by NAT-sub's conditional closure under `a_d, b_d ≥ w_d` (from the divergence-point inequalities via NAT-order), and equal because `a_d = b_d`. At positions `d < i ≤ #a`: both copy their minuends, giving `aᵢ = bᵢ`. The results agree on `1, ..., #a`.

Denote result lengths `L_{a,w}`, `L_{b,w}`. We establish `L_{a,w} ≤ L_{b,w}` by enumerating NAT-order's trichotomy on `(#a, #w)`. In (α) or (γ), `L_{a,w} = #a`; with `#a < #b`, `(#b, #w)` is in (γ), giving `L_{b,w} = #b > #a`. In (β) `#a < #w`, `L_{a,w} = #w`; NAT-order on `(#b, #w)` gives `L_{b,w} ∈ {#b, #w}` with `L_{b,w} ≥ #w = L_{a,w}`.

At positions `#a < i ≤ L_{a,w}` (only in sub-case (β)): `(a ⊖ w)ᵢ = 0` from `a`'s zero-padding, while `(b ⊖ w)ᵢ = bᵢ` or `0` — in either case `(a ⊖ w)ᵢ ≤ (b ⊖ w)ᵢ`.

If a first disagreement exists at `p ∈ 1, ..., L_{a,w}`, then `p > #a` and `(a ⊖ w)_p = 0`, `(b ⊖ w)_p ≠ 0`. By NAT-zero's lower bound and NAT-order's defining clause, `(b ⊖ w)_p > 0`. Position `p` satisfies `p ≤ L_{a,w} ∧ p ≤ L_{b,w}`, so T1 case (i) yields `a ⊖ w < b ⊖ w`. If no disagreement exists, NAT-order's trichotomy at `(L_{a,w}, L_{b,w})` with `L_{a,w} ≤ L_{b,w}` fixes either `L_{a,w} < L_{b,w}` or `L_{a,w} = L_{b,w}`. In the strict case, NAT-discrete gives `L_{a,w} + 1 ≤ L_{b,w}` (with closure by NAT-closure), so `a ⊖ w` is a proper prefix of `b ⊖ w` by T1 case (ii). In the equal case, T3 yields `a ⊖ w = b ⊖ w`.

*Sub-case A3: `a > w` without divergence (zero-padded equality).* The only possibility is T1 case (ii): `w` is a proper prefix of `a` with `aᵢ = 0` for all `i > #w`. NAT-order on `(#a, #w)` is sub-case (γ), giving `L_{a,w} = #a`; `a ⊖ w` is the zero tumbler of that length. Since `#w < #a < #b`, `b` agrees with `w` on `1, ..., #a`, and NAT-order on `(#b, #w)` gives `L_{b,w} = #b`. If `b ⊖ w` has a positive component, `a ⊖ w < b ⊖ w` by TA6. If `b ⊖ w` is also a zero tumbler, both results are zero; NAT-discrete converts `#a < #b` into `#a + 1 ≤ #b`, supplying T1 case (ii)'s witness. Thus `a ⊖ w < b ⊖ w`.

**Case B: Component divergence at `j`** (T1 case (i)). There exists a first position `j` with `j ≤ #a ∧ j ≤ #b`, `aⱼ < bⱼ`, and `aᵢ = bᵢ` for all `i < j`.

*Sub-case B1: `a` is zero-padded-equal to `w`.* Then `a ⊖ w` is the zero tumbler of length `L_{a,w}`. At position `j`, `wⱼ = aⱼ`, so `bⱼ > wⱼ`. The pair `(b, w)` diverges at or before `j`, making `b ⊖ w` positive. By TA6, `a ⊖ w < b ⊖ w`.

For the remaining sub-cases, `dₐ = zpd(a, w)` is well-defined, so TumblerSub's precondition consequence applied to `(a, w)` under `a ≥ w` gives `a_{dₐ} > w_{dₐ}`. The zero-padded divergence `d_b = zpd(b, w)` is also well-defined: if `b` were zero-padded-equal to `w`, then `b_{dₐ} = w_{dₐ}` by that equality, so combined with TumblerSub's consequence, `a_{dₐ} > w_{dₐ} = b_{dₐ}`, while `aᵢ = wᵢ = bᵢ` for `i < dₐ`; Case B's `j` forces `dₐ ≤ j`, giving `dₐ ≤ #a ∧ dₐ ≤ #b`, making `dₐ` a T1 case (i) witness for `a > b` — contradicting `a < b`.

NAT-order's trichotomy on `(dₐ, d_b)` partitions into three sub-cases.

*Sub-case B2: `dₐ = d_b = d`.* For `i < d`, both results are zero. Since `a, b` agree with `w` before `d`, and `aⱼ < bⱼ`, we have `j ≥ d`. If `j = d`: NAT-sub's strict monotonicity at `a_d < b_d` with both `≥ w_d` yields `a_d - w_d < b_d - w_d`, so `a ⊖ w < b ⊖ w` by T1 case (i). If `j > d`: `a_d = b_d`, both results agree at `d`; at `d < i < j`, both copy matching minuend components; at `j`, `(a ⊖ w)ⱼ = aⱼ < bⱼ = (b ⊖ w)ⱼ`. By T1 case (i), `a ⊖ w < b ⊖ w`.

*Sub-case B3: `dₐ < d_b`.* At `dₐ`, `a_{dₐ} ≠ w_{dₐ}` but `b_{dₐ} = w_{dₐ}`. Since `aᵢ = bᵢ` for `i < dₐ`, the first disagreement between `a` and `b` is at `dₐ`, giving `j = dₐ` with `a_{dₐ} < b_{dₐ} = w_{dₐ}`. But TumblerSub's precondition consequence applied to `(a, w)` under `a ≥ w`, with `zpd(a, w) = dₐ` defined, gives `a_{dₐ} > w_{dₐ}` — contradicting `a_{dₐ} < w_{dₐ}`. This case is impossible.

*Sub-case B4: `dₐ > d_b`.* At `d_b`, `b_{d_b} ≠ w_{d_b}` but `a_{d_b} = w_{d_b}`. The first disagreement between `a` and `b` is at `d_b`, giving `j = d_b` with `a_{d_b} = w_{d_b} < b_{d_b}`, where the strict inequality `b_{d_b} > w_{d_b}` comes from TumblerSub's precondition consequence applied to `(b, w)` under `b ≥ w`, with `zpd(b, w) = d_b` defined. Then `(a ⊖ w)_{d_b} = 0` since `d_b < dₐ`, and `(b ⊖ w)_{d_b} = b_{d_b} - w_{d_b} > 0` by NAT-sub's strict positivity. At `i < d_b`, both results are zero. By T1 case (i), `a ⊖ w < b ⊖ w`.

In every case, `a ⊖ w ≤ b ⊖ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
- *Depends:*
  - TA2 (WellDefinedSubtraction) — `a ⊖ w, b ⊖ w ∈ T`; result components in ℕ.
  - TumblerSub (TumblerSub) — component-wise subtraction definition: zero-padding, three-phase formula, length-pair dispatch naming `L_{x,w}`; precondition consequence that when `zpd(x, w)` is defined under `x ≥ w`, `x_{zpd(x,w)} > w_{zpd(x,w)}` holds — invoked in the preamble to Sub-cases B2–B4 to supply `a_{dₐ} > w_{dₐ}`, in Sub-case B3 to contradict `a_{dₐ} < w_{dₐ}`, and in Sub-case B4 applied to `(b, w)` for the strict divergence-point inequality `b_{d_b} > w_{d_b}`; conditional postcondition `Pos(x ⊖ w)` when `zpd(x, w)` is defined — used in Sub-cases A1, A3, and B1 to conclude `b ⊖ w` is positive from the existence of zero-padded divergence.
  - ZPD (ZeroPaddedDivergence) — existence biconditional, first-position characterisation, pre-zpd agreement, Relationship-to-Divergence for the `dₐ ≤ #a` claim under both T1 case (i) and case (ii) for `w < a`.
  - T1 (LexicographicOrder) — strict ordering `<` and derived `≤`; case (i) shared-position bound in conjunction form; case (ii) prefix characterisation.
  - T3 (CanonicalRepresentation) — equality from component-wise agreement at equal length in Sub-case A2's `L_{a,w} = L_{b,w}` branch.
  - TA-Pos (PositiveTumbler) — `Pos(t)` and `Zero(t)` predicates for framing zero-tumbler and positive results of subtractions in Sub-cases A1, A3, B1.
  - TA6 (ZeroTumblers) — a zero tumbler is strictly less than any positive tumbler; used in Sub-cases A1, A3, B1.
  - NAT-sub (NatPartialSubtraction) — conditional closure, strict monotonicity (B2's `j = d` branch), strict positivity (B4).
  - NAT-zero (NatZeroMinimum) — `0 ∈ ℕ` for padded components and literal-zero result components; lower bound at `(b ⊖ w)_p` in Sub-case A2's `≠ 0 ⟹ > 0` step.
  - NAT-order (NatStrictTotalOrder) — trichotomy at `(#a, #w)`, `(#b, #w)`, `(L_{a,w}, L_{b,w})`, `(dₐ, d_b)`; defining clause `m ≤ n ⟺ m < n ∨ m = n` for ≥/> conversions and the `≠ 0 ⟹ > 0` step; transitivity composing length and divergence-position bounds.
  - NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n` supplying T1 case (ii)'s successor witness at `(#a, #b)` in A1 and A3, and at `(L_{a,w}, L_{b,w})` in A2.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(n, 1)` with `1 ∈ ℕ` from the same axiom places `n + 1 ∈ ℕ` for the T1 case (ii) witnesses formed in A1, A2, A3.
- *Postconditions:* a ⊖ w ≤ b ⊖ w
