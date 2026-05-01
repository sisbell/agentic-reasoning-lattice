## What tumbler arithmetic is NOT

**The algebra is not a group.** No additive identity — the zero tumbler is a sentinel. No additive inverse — subtraction is defined only when `a ≥ w`. Not closed under subtraction.

**TA-assoc (AdditionAssociative).** Addition is associative where both compositions are defined: `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` whenever both sides are well-defined.

*Proof.* Write `k_b = actionPoint(b)`, `k_c = actionPoint(c)`. Recall TumblerAdd: for `x ⊕ w` with action point `k`, `(x ⊕ w)ᵢ = xᵢ` for `i < k`, `(x ⊕ w)_k = x_k + w_k`, `(x ⊕ w)ᵢ = wᵢ` for `i > k`, with `#(x ⊕ w) = #w`.

*Lengths.* By TA0: `#(a ⊕ b) = #b`, hence `#((a ⊕ b) ⊕ c) = #c`; and `#(b ⊕ c) = #c`. The outer right-side length `#(a ⊕ (b ⊕ c))` is deferred until `Pos(b ⊕ c)` and `actionPoint(b ⊕ c) ≤ #a` are established.

*Action point of `s = b ⊕ c`.* By TumblerAdd: `sᵢ = bᵢ` for `i < k_c`, `s_{k_c} = b_{k_c} + c_{k_c}`, `sᵢ = cᵢ` for `i > k_c`. NAT-order trichotomy at `k_b, k_c` gives three exhaustive sub-cases; in each we exhibit the least index at which `s` is nonzero and read `actionPoint(s)` off ActionPoint's least-witness clauses.

- `k_b < k_c`: prefix-copy gives `s_{k_b} = b_{k_b}` (since `k_b < k_c`). ActionPoint minimum-nonzero at `b` gives `b_{k_b} ≥ 1`; NAT-zero plus NAT-order's `m ≤ n ⟺ m < n ∨ m = n` lift this to `b_{k_b} > 0`. For `i` with `1 ≤ i < k_b`, `bᵢ = 0` (ActionPoint zeros-below at `b`); since `i < k_b < k_c`, prefix-copy gives `sᵢ = bᵢ = 0`. ActionPoint applied to `s` therefore yields `actionPoint(s) = k_b`.
- `k_b = k_c = k`: `s_k = b_k + c_k`. From `b_k ≥ 1`, `c_k ≥ 1` (ActionPoint minimum-nonzero at `b` and `c`), NAT-addcompat's left order-compatibility gives `b_k + c_k ≥ b_k + 1`; NAT-addcompat's strict successor gives `b_k + 1 > b_k`; NAT-order composes to `b_k + c_k > b_k > 0`. For `i` with `1 ≤ i < k`, `bᵢ = 0` (zeros-below at `b`), and prefix-copy (since `i < k = k_c`) gives `sᵢ = bᵢ = 0`. ActionPoint applied to `s` therefore yields `actionPoint(s) = k`.
- `k_b > k_c`: `b_{k_c} = 0` (ActionPoint zeros-below at `b`, since `k_c < k_b`), so `s_{k_c} = 0 + c_{k_c} = c_{k_c}` by NAT-closure's additive identity; `c_{k_c} ≥ 1` lifts to `c_{k_c} > 0` as above. For `i` with `1 ≤ i < k_c`, `cᵢ = 0` (zeros-below at `c`); since `i < k_c < k_b`, `bᵢ = 0` (zeros-below at `b`), and prefix-copy gives `sᵢ = bᵢ = 0`. ActionPoint applied to `s` therefore yields `actionPoint(s) = k_c`.

In each sub-case the witness index lies in `{1, …, #s}`: `1 ≤ k_b` and `1 ≤ k_c` from ActionPoint's first postcondition at `b` and `c`, and `k_c ≤ #c = #s`, with NAT-order transitivity covering sub-case 1 (where `k_b < k_c ≤ #s`), supplies the upper bound. This witnesses TA-Pos for `s`, so `Pos(s)`. The case-split also yields the unified description: `k_b ≤ k_c ⟹ actionPoint(s) = k_b` (sub-cases 1 and 2) and `k_c ≤ k_b ⟹ actionPoint(s) = k_c` (sub-cases 2 and 3).

*Domain conditions.* Left side requires `Pos(b)`, `k_b ≤ #a`, `Pos(c)`, `k_c ≤ #b` (TA0 on `a ⊕ b` and on `(a ⊕ b) ⊕ c`). Right side requires `Pos(c)`, `k_c ≤ #b`, `Pos(s)`, `actionPoint(s) ≤ #a` (TA0 on `b ⊕ c` and on `a ⊕ s`). The subsumption `k_b ≤ #a ⟹ actionPoint(s) ≤ #a` follows from the case-split: when `k_b ≤ k_c`, `actionPoint(s) = k_b ≤ #a`; when `k_c < k_b`, `actionPoint(s) = k_c < k_b ≤ #a` via NAT-order. The intersection of domains is the formal-contract preconditions.

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
  - T1 (LexicographicOrder) — supplies the `<` and `≥` on tumblers under which TumblerAdd's strict-advancement and dominance postconditions (`a ⊕ w > a`, `a ⊕ w ≥ w`) are stated; TumblerAdd's contract, consumed by this proof, is interpretable only with T1 in scope.
  - T3 (CanonicalRepresentation) — component-wise equality plus equal length implies tumbler equality.
  - NAT-addassoc (NatAdditionAssociative) — `(m + n) + p = m + (n + p)` on ℕ; used in Case 2.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left order-compatibility and strict successor `n < n + 1`; used in sub-case `k_b = k_c`.
  - NAT-cancel (NatAdditionCancellation) — symmetric summand absorption `n + m = m ⟹ n = 0`, on which TumblerAdd's dominance sub-case `aₖ > 0` rests; required in scope for the consumed TumblerAdd contract.
  - NAT-closure (NatArithmeticClosureAndIdentity) — additive identity `0 + n = n` and closure under `+`.
  - NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n`, on which ActionPoint's minimum-nonzero clause `1 ≤ w_{actionPoint(w)}` rests; this proof invokes that clause directly when lifting `b_{k_b} ≥ 1` and `c_{k_c} ≥ 1`.
  - NAT-order (NatStrictTotalOrder) — trichotomy, transitivity, `m ≤ n ⟺ m < n ∨ m = n`.
  - NAT-sub (NatPartialSubtraction) — conditional closure of `k − 1` and `n − k` and the inverse collapses on which TumblerAdd's result-length identity `#(a ⊕ w) = #w` rests; that identity, exported through TA0, supplies the right-side length `#(a ⊕ s) = #c` here.
  - NAT-wellorder (NatWellOrdering) — least-element principle on which ActionPoint's existence-and-uniqueness construction of `actionPoint(w)` rests; this proof invokes ActionPoint's definition and bounds directly when computing `actionPoint(s)` for `s = b ⊕ c` per sub-case of NAT-order trichotomy on `(k_b, k_c)`.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n`; used in `≥ 1 → > 0` lifts.
- *Postconditions:* `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`; `#((a ⊕ b) ⊕ c) = #(a ⊕ (b ⊕ c)) = #c`; `Pos(b ⊕ c)`; `k_b ≤ k_c ⟹ actionPoint(b ⊕ c) = k_b`; `k_c ≤ k_b ⟹ actionPoint(b ⊕ c) = k_c` (jointly characterizing `actionPoint(b ⊕ c)` by NAT-order trichotomy on `(k_b, k_c)`).

**Addition is not commutative.** The operands play asymmetric roles: the first is a *position*, the second a *displacement*. Gregory's `absadd` takes the prefix from the first argument and the suffix from the second.

**There is no multiplication or division.** Gregory's codebase analysis confirms: no `tumblermult`, no `tumblerdiv`. The arithmetic repertoire is add, subtract, increment, compare. Tumblers are addresses, not quantities.

**Tumbler differences are not counts.** Nelson: "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained." The difference between two addresses specifies boundaries, not cardinality. Between sibling addresses 3 and 7, document 5 may have arbitrarily many descendants; their count is unknowable from the addresses alone.
