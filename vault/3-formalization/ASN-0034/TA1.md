**TA1 (OrderPreservationUnderAddition).** `(A a, b, w : a < b ∧ Pos(w) ∧ actionPoint(w) ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`.

TA1 guarantees weak (`≤`) order preservation universally — if two positions were in order before advancement, they remain in non-reversed order after. The precondition `actionPoint(w) ≤ min(#a, #b)` inherits from TA0: both operations must be well-defined.

*Proof.* We show that for all `a, b, w ∈ T` with `a < b`, `Pos(w)`, and `actionPoint(w) ≤ min(#a, #b)`, the advanced positions satisfy `a ⊕ w ≤ b ⊕ w`.

Let `k` be the action point of `w`. By TumblerAdd, the operation `⊕` builds the result in three regions: for `i < k`, `(a ⊕ w)ᵢ = aᵢ` (copy from start); at `i = k`, `(a ⊕ w)ₖ = aₖ + wₖ` (advance); for `i > k`, `(a ⊕ w)ᵢ = wᵢ` (copy from displacement). By TA0, both `a ⊕ w` and `b ⊕ w` are well-defined members of `T` with length `#w`, since `k ≤ min(#a, #b)` ensures the action point falls within both operands. The same three rules apply to `b ⊕ w`.

Since `a < b`, T1 provides exactly two cases: either (i) there exists a least position `j` with `j ≤ min(#a, #b)` where `aⱼ < bⱼ` and `aᵢ = bᵢ` for all `i < j`, or (ii) `a` is a proper prefix of `b`, that is, `#a < #b` and `aᵢ = bᵢ` for all `1 ≤ i ≤ #a`.

*Case (ii): `a` is a proper prefix of `b`.* Here `min(#a, #b) = #a`, so `k ≤ #a`. Since `aᵢ = bᵢ` for all `1 ≤ i ≤ #a` and `k ≤ #a`, the two start positions agree at every position that TumblerAdd consults: for `i < k`, `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`; at `i = k`, `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ` since `aₖ = bₖ`; for `i > k`, `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ`. Both results have length `#w` by TA0. Every component agrees, so `a ⊕ w = b ⊕ w` by T3, satisfying `≤`.

*Case (i): component divergence at position `j`.* Here `j ≤ min(#a, #b)`, `aⱼ < bⱼ`, and `aᵢ = bᵢ` for all `i < j`. Three sub-cases arise from the relationship between the first divergence `j` and the action point `k`.

*Sub-case j < k:* Position `j` falls in the prefix-copy region of TumblerAdd, so `(a ⊕ w)ⱼ = aⱼ` and `(b ⊕ w)ⱼ = bⱼ`, giving `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ`. For all `i < j`, we have `i < j < k`, so both results are in the prefix-copy region and `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ` by the agreement-before-divergence property. Position `j` witnesses T1 case (i): `a ⊕ w < b ⊕ w`.

*Sub-case j = k:* For all `i < k = j`, both results are in the prefix-copy region and `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ` by agreement before the divergence. At position `k`, `(a ⊕ w)ₖ = aₖ + wₖ` and `(b ⊕ w)ₖ = bₖ + wₖ`. Since `aₖ < bₖ` (the divergence at `j = k`) and addition of a fixed natural number preserves strict inequality on ℕ, we have `aₖ + wₖ < bₖ + wₖ`. Position `k` witnesses T1 case (i): `a ⊕ w < b ⊕ w`.

*Sub-case j > k:* Since `k < j` and `aᵢ = bᵢ` for all `i < j`, in particular `aₖ = bₖ` (because `k < j`). For `i < k`: both results are in the prefix-copy region, and `i < k < j` gives `aᵢ = bᵢ`, so `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At position `k`: `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ` since `aₖ = bₖ`. For `i > k`: both results copy from the displacement, so `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ`. Both results have length `#w` by TA0. Every component agrees, so `a ⊕ w = b ⊕ w` by T3, satisfying `≤`.

In every case and sub-case, `a ⊕ w ≤ b ⊕ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, Pos(w), actionPoint(w) ≤ min(#a, #b)
- *Depends:* TA0 (WellDefinedAddition) — both `a ⊕ w` and `b ⊕ w` must be well-defined members of T with length `#w`. TumblerAdd (TumblerAdd) — the three-region piecewise structure determines how each component of the result is computed. T1 (LexicographicOrder) — case analysis on the ordering `a < b` drives the proof structure, and T1 case (i) establishes the ordering of the results. T3 (CanonicalRepresentation) — component-wise agreement with equal length concludes `a ⊕ w = b ⊕ w` in the prefix and j > k sub-cases.
- *Postconditions:* a ⊕ w ≤ b ⊕ w

Strict order preservation holds under a tighter condition. We first need a precise notion of where two tumblers first differ.
