**ReverseInverse (ReverseInverse).** `(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`.

*Proof.* We show that subtracting `w` from `a` and then adding `w` back recovers `a` exactly, under conditions that make the two operations mutually inverse. Throughout, `k` denotes the action point of `w` — the least position with `wₖ > 0` — so by definition `wᵢ = 0` for all `i < k`.

**Step 1: the structure of `y = a ⊖ w`.** By TumblerSub, subtraction scans `a` and `w` for the first position where they differ, zero-padding the shorter to length `max(#a, #w)`. Since `#a = k = #w` (given), no padding is needed. At each position `i < k`, both `aᵢ = 0` (by the zero-prefix precondition) and `wᵢ = 0` (by definition of action point), so the operands agree before position `k`.

Two cases arise at position `k`. If `aₖ = wₖ`, then `a` and `w` agree at every position — there are no positions beyond `k` since both have length `k` — and TumblerSub produces the zero tumbler of length `k`. If `aₖ > wₖ` (the only alternative, since `a ≥ w` excludes `aₖ < wₖ`), then `k` is the first divergence, and TumblerSub produces `yᵢ = 0` for `i < k`, `yₖ = aₖ - wₖ > 0`, and no components beyond `k` (since `max(#a, #w) = k`). In either case, `y` has three properties we record for later use:

- (Y1) `#y = k`
- (Y2) `yᵢ = 0` for all `1 ≤ i < k`
- (Y3) `yₖ = aₖ - wₖ`

**Step 2: TA4 applies to `y` and `w`.** TA4 (Partial inverse) requires four preconditions: `w > 0` (given), `k = #y` (by Y1), `#w = k` (given), and `(A i : 1 ≤ i < k : yᵢ = 0)` (by Y2). All four hold, so TA4 yields:

`(y ⊕ w) ⊖ w = y`  — (†)

**Step 3: `y ⊕ w = a` by contradiction via TA3-strict.** Assume for contradiction that `y ⊕ w ≠ a`. We verify the preconditions of TA3-strict (Order preservation under subtraction, strict), which requires strict ordering between two tumblers, both `≥ w`, and equal length.

*Equal length.* By the result-length identity (TumblerAdd), `#(y ⊕ w) = #w`. The preconditions give `#w = k` and `k = #a`, so `#(y ⊕ w) = #a`.

*`a ≥ w`.* Given as a precondition of ReverseInverse.

*`y ⊕ w > w`.* By TumblerAdd, for `i < k`: `(y ⊕ w)ᵢ = yᵢ = 0 = wᵢ` (using Y2 and the definition of action point). At position `k`: `(y ⊕ w)ₖ = yₖ + wₖ`. Since `#(y ⊕ w) = k = #w`, there are no positions beyond `k`, so the two tumblers `y ⊕ w` and `w` agree at all positions except possibly `k`. We show `yₖ > 0`. If `yₖ = 0`, then by Y3, `aₖ = wₖ`. Combined with `aᵢ = wᵢ = 0` for all `i < k` and `#a = #w = k`, this gives `a = w` by T3 (CanonicalRepresentation). Then `y = a ⊖ w = w ⊖ w`, which is the zero tumbler of length `k`, and `y ⊕ w` has `(y ⊕ w)ₖ = 0 + wₖ = wₖ` with zeros before `k`, so `y ⊕ w = w = a` — contradicting our assumption. Therefore `yₖ > 0`, giving `(y ⊕ w)ₖ = yₖ + wₖ > wₖ`. The two tumblers agree before `k` and first differ at `k` with `(y ⊕ w)ₖ > wₖ`, so by T1, `y ⊕ w > w`.

*Strict ordering between `y ⊕ w` and `a`.* By T1 (trichotomy), since `y ⊕ w ≠ a`, exactly one of `y ⊕ w < a` or `y ⊕ w > a` holds. We derive a contradiction from each.

*Case `y ⊕ w > a`:* We have `a < y ⊕ w`, `a ≥ w`, `y ⊕ w ≥ w` (established above, in fact strict), and `#a = #(y ⊕ w)`. TA3-strict gives `a ⊖ w < (y ⊕ w) ⊖ w`. The left side is `y` by definition; the right side is `y` by (†). This yields `y < y`, contradicting the irreflexivity of `<` (T1).

*Case `y ⊕ w < a`:* We have `y ⊕ w < a`, `y ⊕ w ≥ w` (strict), `a ≥ w`, and `#(y ⊕ w) = #a`. TA3-strict gives `(y ⊕ w) ⊖ w < a ⊖ w`. The left side is `y` by (†); the right side is `y` by definition. This yields `y < y`, again contradicting irreflexivity.

Both cases are impossible, so the assumption `y ⊕ w ≠ a` is false. Therefore `(a ⊖ w) ⊕ w = a`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Postconditions:* `(a ⊖ w) ⊕ w = a`
