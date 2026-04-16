**TA-MTO (ManyToOne).** For any displacement w with action point k and any tumblers a, b with #a ≥ k and #b ≥ k: a ⊕ w = b ⊕ w if and only if a_i = b_i for all 1 ≤ i ≤ k.

*Proof.* We establish an equivalence: two tumblers produce the same result under a displacement if and only if they agree on every component up to and including the action point.

Let `w` be a displacement with action point `k`, and let `a, b ∈ T` with `#a ≥ k` and `#b ≥ k`. Both additions `a ⊕ w` and `b ⊕ w` are well-defined by TA0, since the action point `k` falls within both operands' lengths. TumblerAdd's constructive definition (Definition TumblerAdd) builds each result in three regions relative to `k`:

```
  (a ⊕ w)ᵢ = aᵢ         for 1 ≤ i < k     (prefix copy from start)
  (a ⊕ w)ₖ = aₖ + wₖ                       (single-component advance)
  (a ⊕ w)ᵢ = wᵢ         for k < i ≤ #w     (tail copy from displacement)
```

and identically for `b ⊕ w` with `bᵢ` replacing `aᵢ`. The result-length identity (TumblerAdd) gives `#(a ⊕ w) = #w = #(b ⊕ w)`.

*(Forward: agreement implies equal results.)* Assume `aᵢ = bᵢ` for all `1 ≤ i ≤ k`. We show `(a ⊕ w)ᵢ = (b ⊕ w)ᵢ` at every position `i` from `1` to `#w`, which together with `#(a ⊕ w) = #(b ⊕ w) = #w` yields `a ⊕ w = b ⊕ w` by T3 (CanonicalRepresentation).

*Position i < k:* `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. The first equality is TumblerAdd's prefix-copy rule; the second is the hypothesis `aᵢ = bᵢ`; the third is the prefix-copy rule applied to `b`.

*Position i = k:* `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ`. The middle step uses the hypothesis `aₖ = bₖ`.

*Position i > k:* `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ`. Both results take their tail from `w`; neither `a` nor `b` contributes to these positions.

All components agree and the lengths are equal, so `a ⊕ w = b ⊕ w` by T3.

*(Converse: equal results implies agreement.)* Assume `a ⊕ w = b ⊕ w`. By T3 (CanonicalRepresentation), this entails `(a ⊕ w)ᵢ = (b ⊕ w)ᵢ` at every position. We extract `aᵢ = bᵢ` for each `1 ≤ i ≤ k`.

*Position i < k:* TumblerAdd's prefix-copy rule gives `(a ⊕ w)ᵢ = aᵢ` and `(b ⊕ w)ᵢ = bᵢ`. From `(a ⊕ w)ᵢ = (b ⊕ w)ᵢ` we obtain `aᵢ = bᵢ`.

*Position i = k:* TumblerAdd's advance rule gives `(a ⊕ w)ₖ = aₖ + wₖ` and `(b ⊕ w)ₖ = bₖ + wₖ`. From `(a ⊕ w)ₖ = (b ⊕ w)ₖ` we obtain `aₖ + wₖ = bₖ + wₖ`, hence `aₖ = bₖ` by cancellation in ℕ.

Positions `i > k` impose no constraint on `a` or `b`: `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ` holds regardless of `aᵢ` and `bᵢ`, since TumblerAdd's tail-copy rule draws these components entirely from `w`. ∎

This gives a precise characterization of the equivalence classes: *a and b produce the same result under w if and only if they agree on the first k components, where k is the action point of w.*

*Formal Contract:*
- *Preconditions:* w ∈ T, Pos(w), a ∈ T, b ∈ T, #a ≥ actionPoint(w), #b ≥ actionPoint(w)
- *Postconditions:* a ⊕ w = b ⊕ w ⟺ (A i : 1 ≤ i ≤ actionPoint(w) : aᵢ = bᵢ)
