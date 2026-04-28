**Prefix (PrefixRelation).** The prefix relation on tumblers: `p ≼ q` iff `#p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. A proper prefix `p ≺ q` requires `p ≼ q` with `p ≠ q`. We write `p ⋠ q` for the negation `¬(p ≼ q)` — read "p is not a prefix of q".

*Formal Contract:*
- *Definition:* `p ≼ q` iff `#p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. Proper prefix: `p ≺ q` iff `p ≼ q ∧ p ≠ q`. Non-prefix: `p ⋠ q` iff `¬(p ≼ q)`.
- *Depends:*
  - T0 (CarrierSetDefinition) — length `#p` and component projection `pᵢ` for `p ∈ T`.
  - NAT-order (NatStrictTotalOrder) — `≤` on ℕ for length comparison and index range; defining clause `m ≤ n ⟺ m < n ∨ m = n`.
  - T3 (CanonicalRepresentation) — equal-length tumblers agreeing on all components are equal.
- *Derived postcondition (proper-prefix length):* `p ≺ q ⟹ #p < #q`. From `p ≼ q` conclude `#p ≤ #q`. If `#p = #q`, the component condition `(∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)` covers all positions of both tumblers, so by T3 `p = q`, contradicting `p ≠ q`. Hence `#p ≠ #q`, and by NAT-order's `≤`-unfolding `#p < #q`.
- *Derived postcondition (reflexivity):* `(∀t ∈ T :: t ≼ t)`. Instantiate the Definition at `p = q = t`: `#t ≤ #t` by NAT-order's `≤`-clause at the equality disjunct; `tᵢ = tᵢ` for `1 ≤ i ≤ #t` by reflexivity of equality. Both conjuncts hold, so `t ≼ t`.
