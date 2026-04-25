**TA-MTO (ManyToOne).** For any displacement w with action point k and any tumblers a, b with #a ≥ k and #b ≥ k: a ⊕ w = b ⊕ w if and only if a_i = b_i for all 1 ≤ i ≤ k.

*Proof.* Let `w` be a displacement with action point `k`, and let `a, b ∈ T` with `#a ≥ k` and `#b ≥ k`. Both additions `a ⊕ w` and `b ⊕ w` are well-defined by TA0. TumblerAdd builds each result in three regions relative to `k`:

```
  (a ⊕ w)ᵢ = aᵢ         for 1 ≤ i < k     (prefix copy)
  (a ⊕ w)ₖ = aₖ + wₖ                       (advance)
  (a ⊕ w)ᵢ = wᵢ         for k < i ≤ #w     (tail copy)
```

and identically for `b ⊕ w`. TumblerAdd gives `#(a ⊕ w) = #w = #(b ⊕ w)`.

*(Forward.)* Assume `aᵢ = bᵢ` for all `1 ≤ i ≤ k`.

*Position i < k:* `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ` by prefix-copy and the hypothesis.

*Position i = k:* `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ` by advance and the hypothesis.

*Position i > k:* `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ` by tail-copy.

All components agree and lengths are equal, so `a ⊕ w = b ⊕ w` by T3.

*(Converse.)* Assume `a ⊕ w = b ⊕ w`. By T3, `(a ⊕ w)ᵢ = (b ⊕ w)ᵢ` at every position.

*Position i < k:* prefix-copy gives `(a ⊕ w)ᵢ = aᵢ` and `(b ⊕ w)ᵢ = bᵢ`, so `aᵢ = bᵢ`.

*Position i = k:* advance gives `aₖ + wₖ = bₖ + wₖ`, hence `aₖ = bₖ` by NAT-cancel with `m = wₖ`. ∎

*Formal Contract:*
- *Preconditions:* w ∈ T, Pos(w), a ∈ T, b ∈ T, #a ≥ actionPoint(w), #b ≥ actionPoint(w)
- *Depends:*
  - TumblerAdd (TumblerAdd) — three-region constructive definition and result-length identity.
  - TA0 (WellDefinedAddition) — well-definedness of `a ⊕ w` and `b ⊕ w`.
  - TA-Pos (PositiveTumbler) — discharges `Pos(w)` for TA0 and ActionPoint.
  - ActionPoint (ActionPoint) — names `k` and licenses the three-region split.
  - T3 (CanonicalRepresentation) — position-wise-and-length characterisation of tumbler equality.
  - NAT-cancel (NatAdditionCancellation) — right cancellation on ℕ at position `k`.
- *Postconditions:* a ⊕ w = b ⊕ w ⟺ (A i : 1 ≤ i ≤ actionPoint(w) : aᵢ = bᵢ)
