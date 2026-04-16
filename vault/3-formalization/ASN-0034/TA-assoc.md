## What tumbler arithmetic is NOT

We must state explicitly what the tumbler algebra does not guarantee. These negative results constrain what an implementer may assume.

**The algebra is not a group.** There is no additive identity — the zero tumbler is a sentinel, not a neutral element for addition. There is no additive inverse for every element — subtraction is only defined when `a ≥ w`. The algebra is not closed under subtraction in general.

**TA-assoc (AdditionAssociative).** Addition is associative where both compositions are defined: `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` whenever both sides are well-defined. Three cases exhaust the possibilities. Let `k_b` and `k_c` be the action points of `b` and `c` respectively. When `k_b < k_c`: both sides produce `aᵢ` for `i < k_b`, `aₖ_b + bₖ_b` at `k_b`, `bᵢ` for `k_b < i < k_c`, `bₖ_c + cₖ_c` at `k_c`, and `cᵢ` beyond — identical. When `k_b = k_c = k`: both sides produce `aₖ + bₖ + cₖ` at `k` (natural-number addition is associative) and `cᵢ` beyond — identical. When `k_b > k_c`: both sides produce `aₖ_c + cₖ_c` at `k_c` and `cᵢ` beyond — identical (the deeper displacement `b` is overwritten by the shallower `c` in both cases). The domain conditions are asymmetric — the left side requires `k_b ≤ #a`, while the right requires only `min(k_b, k_c) ≤ #a` — but on the intersection, the values agree.

The design does not depend on associativity. Shifts are applied as single operations in practice, never composed from multiple smaller shifts. An implementation with finite representations may break associativity through overflow at the action-point component, but the abstract algebra carries no such limitation.

*Proof.* We show that for all `a, b, c ∈ T` with `Pos(b)`, `Pos(c)`, whenever both `(a ⊕ b) ⊕ c` and `a ⊕ (b ⊕ c)` are well-defined, every component of the left side equals the corresponding component of the right side.

Throughout, write `k_b` for the action point of `b` and `k_c` for the action point of `c`. Recall TumblerAdd's constructive definition: for `x ⊕ w` with `w` having action point `k`, the result has `(x ⊕ w)ᵢ = xᵢ` for `i < k` (prefix copy), `(x ⊕ w)ₖ = xₖ + wₖ` (advance), and `(x ⊕ w)ᵢ = wᵢ` for `i > k` (tail copy), with `#(x ⊕ w) = #w` (the result-length identity from TA0).

*Lengths.* By the result-length identity, `#(a ⊕ b) = #b`. Applying it again: `#((a ⊕ b) ⊕ c) = #c`. For the right side, `#(b ⊕ c) = #c`, and `#(a ⊕ (b ⊕ c)) = #(b ⊕ c) = #c`. Both sides have length `#c`.

*Action point of `s = b ⊕ c`.* We must determine `actionPoint(s)` to expand the right side `a ⊕ s`. By TumblerAdd on `b ⊕ c`: `sᵢ = bᵢ` for `i < k_c`, `s_{k_c} = b_{k_c} + c_{k_c}`, and `sᵢ = cᵢ` for `i > k_c`. The action point of `s` is the first position with a nonzero component. For `i < min(k_b, k_c)`, we have `i < k_b` (so `bᵢ = 0` by definition of action point) and `i < k_c` (so `sᵢ = bᵢ = 0` by the prefix-copy rule). At position `min(k_b, k_c)` three sub-cases arise. If `k_b < k_c`: `s_{k_b} = b_{k_b} > 0`, since `k_b` is the action point of `b` and `k_b < k_c` places it in the prefix-copy region. If `k_b = k_c`: `s_{k_b} = b_{k_b} + c_{k_b} > 0`, since both summands are positive action-point values. If `k_b > k_c`: `s_{k_c} = b_{k_c} + c_{k_c} = 0 + c_{k_c} = c_{k_c} > 0`, since `k_c < k_b` gives `b_{k_c} = 0`. In every sub-case the first nonzero component of `s` occurs at position `min(k_b, k_c)`, establishing `actionPoint(s) = min(k_b, k_c)`.

*Domain conditions.* The left side `(a ⊕ b) ⊕ c` requires two well-defined additions: `a ⊕ b` requires `k_b ≤ #a` (TA0), and `(a ⊕ b) ⊕ c` requires `k_c ≤ #(a ⊕ b) = #b` (TA0 applied to the intermediate result). The right side `a ⊕ (b ⊕ c)` requires `b ⊕ c` with `k_c ≤ #b` (TA0), and `a ⊕ s` with `actionPoint(s) = min(k_b, k_c) ≤ #a` (TA0). The domains are asymmetric: the left requires `k_b ≤ #a`, the right requires only `min(k_b, k_c) ≤ #a`. But since `k_b ≤ #a` implies `min(k_b, k_c) ≤ #a`, the left-side conditions subsume the right-side conditions. The intersection of both domains is therefore `k_b ≤ #a` and `k_c ≤ #b`. We assume these hold and show the values agree by exhaustive case analysis on the relationship between `k_b` and `k_c`.

*Case 1: `k_b < k_c`.* The action point of `s` is `k_b`, with `s_{k_b} = b_{k_b}` (from the prefix-copy region of `b ⊕ c`, since `k_b < k_c`).

Let `r = a ⊕ b`. By TumblerAdd: `rᵢ = aᵢ` for `i < k_b`, `r_{k_b} = a_{k_b} + b_{k_b}`, and `rᵢ = bᵢ` for `i > k_b`.

*Left side* `(r ⊕ c)` with action point `k_c`: for `i < k_b` we have `i < k_c`, so `(r ⊕ c)ᵢ = rᵢ = aᵢ`. At `i = k_b < k_c`: position `k_b` falls in the prefix-copy region of `r ⊕ c`, so `(r ⊕ c)_{k_b} = r_{k_b} = a_{k_b} + b_{k_b}`. For `k_b < i < k_c`: `(r ⊕ c)ᵢ = rᵢ = bᵢ` (prefix-copy from `r`, and `i > k_b` puts `rᵢ` in the tail-copy region of `a ⊕ b`). At `i = k_c`: `(r ⊕ c)_{k_c} = r_{k_c} + c_{k_c} = b_{k_c} + c_{k_c}`, since `k_c > k_b` gives `r_{k_c} = b_{k_c}` by the tail-copy rule of `a ⊕ b`. For `i > k_c`: `(r ⊕ c)ᵢ = cᵢ`.

*Right side* `(a ⊕ s)` with action point `k_b`: for `i < k_b`, `(a ⊕ s)ᵢ = aᵢ`. At `i = k_b`: `(a ⊕ s)_{k_b} = a_{k_b} + s_{k_b} = a_{k_b} + b_{k_b}`. For `i > k_b`: `(a ⊕ s)ᵢ = sᵢ` by the tail-copy rule. Expanding `sᵢ` via TumblerAdd on `b ⊕ c`: for `k_b < i < k_c`, `sᵢ = bᵢ` (prefix-copy, since `i < k_c`); at `i = k_c`, `s_{k_c} = b_{k_c} + c_{k_c}` (advance); for `i > k_c`, `sᵢ = cᵢ` (tail-copy).

Comparing position by position: `aᵢ = aᵢ` for `i < k_b`; `a_{k_b} + b_{k_b} = a_{k_b} + b_{k_b}` at `k_b`; `bᵢ = bᵢ` for `k_b < i < k_c`; `b_{k_c} + c_{k_c} = b_{k_c} + c_{k_c}` at `k_c`; `cᵢ = cᵢ` for `i > k_c`. Every component agrees.

*Case 2: `k_b = k_c = k`.* The action point of `s` is `k`, with `s_k = b_k + c_k`.

Let `r = a ⊕ b`: `rᵢ = aᵢ` for `i < k`, `r_k = a_k + b_k`, `rᵢ = bᵢ` for `i > k`. The left side `(r ⊕ c)` has action point `k`: for `i < k`, `(r ⊕ c)ᵢ = rᵢ = aᵢ`; at `k`, `(r ⊕ c)_k = r_k + c_k = (a_k + b_k) + c_k`; for `i > k`, `(r ⊕ c)ᵢ = cᵢ`. The right side `(a ⊕ s)` has action point `k`: for `i < k`, `(a ⊕ s)ᵢ = aᵢ`; at `k`, `(a ⊕ s)_k = a_k + s_k = a_k + (b_k + c_k)`; for `i > k`, `(a ⊕ s)ᵢ = sᵢ = cᵢ`.

At position `k`, the left gives `(a_k + b_k) + c_k` and the right gives `a_k + (b_k + c_k)`. These are equal by associativity of addition on ℕ. All other positions agree by direct comparison.

*Case 3: `k_b > k_c`.* The action point of `s` is `k_c`, with `s_{k_c} = b_{k_c} + c_{k_c} = 0 + c_{k_c} = c_{k_c}` (since `k_c < k_b` gives `b_{k_c} = 0`).

Let `r = a ⊕ b`: `rᵢ = aᵢ` for `i < k_b`, `r_{k_b} = a_{k_b} + b_{k_b}`, `rᵢ = bᵢ` for `i > k_b`. The left side `(r ⊕ c)` has action point `k_c`. Since `k_c < k_b`: for `i < k_c` we have `i < k_b`, so `(r ⊕ c)ᵢ = rᵢ = aᵢ` (both prefix-copy rules apply). At `i = k_c < k_b`: `r_{k_c} = a_{k_c}` (position `k_c` falls in the prefix-copy region of `a ⊕ b`), so `(r ⊕ c)_{k_c} = r_{k_c} + c_{k_c} = a_{k_c} + c_{k_c}`. For `i > k_c`: `(r ⊕ c)ᵢ = cᵢ`. The components of `r` at and beyond `k_b` — where `b`'s contribution appears — are entirely overwritten by `c`'s tail, since `k_c < k_b`.

The right side `(a ⊕ s)` has action point `k_c`: for `i < k_c`, `(a ⊕ s)ᵢ = aᵢ`; at `k_c`, `(a ⊕ s)_{k_c} = a_{k_c} + s_{k_c} = a_{k_c} + c_{k_c}`; for `i > k_c`, `(a ⊕ s)ᵢ = sᵢ = cᵢ` (since `sᵢ = cᵢ` for `i > k_c` by the tail-copy rule of `b ⊕ c`).

Comparing: `aᵢ = aᵢ` for `i < k_c`; `a_{k_c} + c_{k_c} = a_{k_c} + c_{k_c}` at `k_c`; `cᵢ = cᵢ` for `i > k_c`. Every component agrees. The displacement `b` is entirely overwritten — TumblerAdd's tail-replacement semantics means the shallower displacement `c` discards everything below its action point on both sides, rendering `b`'s deeper contribution invisible in the final result.

In all three cases, both sides produce the same sequence of length `#c`, so `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` by T3 (CanonicalRepresentation). ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `b ∈ T`, `c ∈ T`, `Pos(b)`, `Pos(c)`, `k_b ≤ #a`, `k_c ≤ #b` (where `k_b = actionPoint(b)`, `k_c = actionPoint(c)`; these left-side conditions subsume the right-side conditions since `k_b ≤ #a` implies `min(k_b, k_c) ≤ #a`)
- *Postconditions:* `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`; `#((a ⊕ b) ⊕ c) = #(a ⊕ (b ⊕ c)) = #c`; `actionPoint(b ⊕ c) = min(k_b, k_c)`

**Addition is not commutative.** We do NOT require `a ⊕ b = b ⊕ a`. The operands play asymmetric roles: the first is a *position*, the second is a *displacement*. Swapping them is semantically meaningless. Gregory's `absadd` confirms: the first argument supplies the prefix, the second the suffix — the reverse call gives a different (and typically wrong) result.

**There is no multiplication or division.** Gregory's analysis of the complete codebase confirms: no `tumblermult`, no `tumblerdiv`, no scaling operation of any kind. The arithmetic repertoire is: add, subtract, increment, compare. Tumblers are *addresses*, not quantities. You don't multiply two file paths or divide an address by three.

**Tumbler differences are not counts.** Nelson is emphatic: "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." The difference between two addresses specifies *boundaries*, not *cardinality*. What lies between those boundaries depends on the actual population of the tree, which is dynamic and unpredictable. Between sibling addresses 3 and 7, document 5 might have arbitrarily many descendants — the span from 3 to 7 encompasses all of them, and their count is unknowable from the addresses alone. The arithmetic is an *addressing calculus*, not a *counting calculus*.

The absence of algebraic structure beyond a monotone shift is not a deficiency. It is the *minimum* that addressing requires. An ordered set with an order-preserving shift and an allocation increment is sufficient. Anything more would be unused machinery and unverified obligation.
