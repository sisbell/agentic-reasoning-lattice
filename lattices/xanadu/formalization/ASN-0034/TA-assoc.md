## What tumbler arithmetic is NOT

**The algebra is not a group.** No additive identity — the zero tumbler is a sentinel. No additive inverse — subtraction is defined only when `a ≥ w`. Not closed under subtraction.

**TA-assoc (AdditionAssociative).** Addition is associative where both compositions are defined: `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` whenever both sides are well-defined.

*Proof.* Write `k_b = actionPoint(b)`, `k_c = actionPoint(c)`. Recall TumblerAdd: for `x ⊕ w` with action point `k`, `(x ⊕ w)ᵢ = xᵢ` for `i < k`, `(x ⊕ w)_k = x_k + w_k`, `(x ⊕ w)ᵢ = wᵢ` for `i > k`, with `#(x ⊕ w) = #w`.

*Lengths.* By TA0: `#(a ⊕ b) = #b`, hence `#((a ⊕ b) ⊕ c) = #c`; and `#(b ⊕ c) = #c`. The outer right-side length `#(a ⊕ (b ⊕ c))` is deferred until `Pos(b ⊕ c)` and `actionPoint(b ⊕ c) ≤ #a` are established.

*Action point of `s = b ⊕ c`.* By TumblerAdd: `sᵢ = bᵢ` for `i < k_c`, `s_{k_c} = b_{k_c} + c_{k_c}`, `sᵢ = cᵢ` for `i > k_c`. For `i < min(k_b, k_c)`, `bᵢ = 0` (ActionPoint zeros-below) and `sᵢ = bᵢ = 0`. NAT-order trichotomy at `k_b, k_c` gives three exhaustive sub-cases:

- `k_b < k_c`: `s_{k_b} = b_{k_b}` (prefix-copy). ActionPoint minimum-nonzero gives `b_{k_b} ≥ 1`; NAT-zero plus NAT-order's `m ≤ n ⟺ m < n ∨ m = n` lift this to `b_{k_b} > 0`.
- `k_b = k_c = k`: `s_k = b_k + c_k`. From `b_k ≥ 1`, `c_k ≥ 1` (ActionPoint), NAT-addcompat's left order-compatibility gives `b_k + c_k ≥ b_k + 1`; NAT-addcompat's strict successor gives `b_k + 1 > b_k`; NAT-order composes to `b_k + c_k > b_k > 0`.
- `k_b > k_c`: `b_{k_c} = 0` (ActionPoint zeros-below), so `s_{k_c} = 0 + c_{k_c} = c_{k_c}` by NAT-closure's additive identity; `c_{k_c} ≥ 1` lifts to `c_{k_c} > 0` as above.

In every sub-case `s` is nonzero at `min(k_b, k_c)`. ActionPoint's first postcondition at `b` and `c` supplies `1 ≤ k_b` and `1 ≤ k_c`, hence `1 ≤ min(k_b, k_c)`; `k_c ≤ #c = #s` gives the upper bound (with NAT-order transitivity handling the sub-case `k_b < k_c`). This witnesses TA-Pos at `i = min(k_b, k_c)`, so `Pos(s)`. ActionPoint's definition applied to `s` yields `actionPoint(s) = min(k_b, k_c)`.

*Domain conditions.* Left side requires `Pos(b)`, `k_b ≤ #a`, `Pos(c)`, `k_c ≤ #b` (TA0 on `a ⊕ b` and on `(a ⊕ b) ⊕ c`). Right side requires `Pos(c)`, `k_c ≤ #b`, `Pos(s)`, `actionPoint(s) ≤ #a` (TA0 on `b ⊕ c` and on `a ⊕ s`). The subsumption `k_b ≤ #a ⟹ min(k_b, k_c) ≤ #a` holds by trichotomy: when `k_b ≤ k_c`, `min = k_b`; when `k_b > k_c`, `min = k_c < k_b ≤ #a` via NAT-order. The intersection of domains is the formal-contract preconditions.

*Right-side length.* With `Pos(s)` and `actionPoint(s) ≤ #a`, TA0 gives `#(a ⊕ s) = #s = #c`. Both sides have length `#c`.

*Case 1: `k_b < k_c`.* `actionPoint(s) = k_b`, `s_{k_b} = b_{k_b}`. Let `r = a ⊕ b`.

Left `(r ⊕ c)` has action point `k_c`: `aᵢ` for `i < k_b`; `r_{k_b} = a_{k_b} + b_{k_b}` at `k_b`; `rᵢ = bᵢ` for `k_b < i < k_c`; `r_{k_c} + c_{k_c} = b_{k_c} + c_{k_c}` at `k_c`; `cᵢ` for `i > k_c`.

Right `(a ⊕ s)` has action point `k_b`: `aᵢ` for `i < k_b`; `a_{k_b} + s_{k_b} = a_{k_b} + b_{k_b}` at `k_b`; `sᵢ = bᵢ` for `k_b < i < k_c`; `s_{k_c} = b_{k_c} + c_{k_c}` at `k_c`; `cᵢ` for `i > k_c`.

Every component agrees.

*Case 2: `k_b = k_c = k`.* `actionPoint(s) = k`, `s_k = b_k + c_k`. Let `r = a ⊕ b`.

Left `(r ⊕ c)_k = r_k + c_k = (a_k + b_k) + c_k`. Right `(a ⊕ s)_k = a_k + s_k = a_k + (b_k + c_k)`. Equal by NAT-addassoc. All other positions match directly.

*Case 3: `k_b > k_c`.* `actionPoint(s) = k_c`, `s_{k_c} = 0 + c_{k_c} = c_{k_c}`. Let `r = a ⊕ b`.

Left `(r ⊕ c)` has action point `k_c`: for `i < k_c < k_b`, `rᵢ = aᵢ`; at `k_c`, `r_{k_c} + c_{k_c} = a_{k_c} + c_{k_c}`; for `i > k_c`, `cᵢ`.

Right `(a ⊕ s)` has action point `k_c`: `aᵢ` for `i < k_c`; `a_{k_c} + s_{k_c} = a_{k_c} + c_{k_c}` at `k_c`; `sᵢ = cᵢ` for `i > k_c`.

Every component agrees. The shallower displacement `c` discards everything below its action point on both sides, so `b`'s contribution at and beyond `k_b` is invisible.

In all three cases both sides produce the same sequence of length `#c`, so `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` by T3. ∎

*Formal Contract:*
- *Preconditions:* `a, b, c ∈ T`, `Pos(b)`, `Pos(c)`, `k_b ≤ #a`, `k_c ≤ #b` (where `k_b = actionPoint(b)`, `k_c = actionPoint(c)`).
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T` and length `#·` on finite ℕ-sequences.
  - TumblerAdd (TumblerAdd) — piecewise prefix-copy / advance / tail-copy definition of `⊕`.
  - TA0 (WellDefinedAddition) — preconditions `Pos(w)`, `actionPoint(w) ≤ #x`; result-length `#(x ⊕ w) = #w`.
  - TA-Pos (PositiveTumbler) — existential definition of `Pos(·)`; consumed to establish `Pos(b ⊕ c)`.
  - ActionPoint (ActionPoint) — definition `actionPoint(w) = min{i : wᵢ ≠ 0}`; bounds `1 ≤ actionPoint(w) ≤ #w`; zeros-below; minimum-nonzero `w_{actionPoint(w)} ≥ 1`.
  - T3 (CanonicalRepresentation) — component-wise equality plus equal length implies tumbler equality.
  - NAT-addassoc (NatAdditionAssociative) — `(m + n) + p = m + (n + p)` on ℕ; used in Case 2.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left order-compatibility and strict successor `n < n + 1`; used in sub-case `k_b = k_c`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — additive identity `0 + n = n` and closure under `+`.
  - NAT-order (NatStrictTotalOrder) — trichotomy, transitivity, `m ≤ n ⟺ m < n ∨ m = n`.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n`; used in `≥ 1 → > 0` lifts.
- *Postconditions:* `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`; `#((a ⊕ b) ⊕ c) = #(a ⊕ (b ⊕ c)) = #c`; `Pos(b ⊕ c)`; `actionPoint(b ⊕ c) = min(k_b, k_c)`.

**Addition is not commutative.** The operands play asymmetric roles: the first is a *position*, the second a *displacement*. Gregory's `absadd` takes the prefix from the first argument and the suffix from the second.

**There is no multiplication or division.** Gregory's codebase analysis confirms: no `tumblermult`, no `tumblerdiv`. The arithmetic repertoire is add, subtract, increment, compare. Tumblers are addresses, not quantities.

**Tumbler differences are not counts.** Nelson: "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained." The difference between two addresses specifies boundaries, not cardinality. Between sibling addresses 3 and 7, document 5 may have arbitrarily many descendants; their count is unknowable from the addresses alone.
