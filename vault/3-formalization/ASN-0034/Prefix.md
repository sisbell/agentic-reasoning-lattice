**Definition (Prefix).** The prefix relation on tumblers: `p ≼ q` iff `#p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. A proper prefix `p ≺ q` requires `p ≼ q` with `p ≠ q`. This entails `#p < #q`: if `#p = #q`, then the prefix condition `(∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)` covers all positions of both tumblers, and T3 (CanonicalRepresentation) gives `p = q`, contradicting `p ≠ q`.

*Formal Contract:*
- *Definition:* `p ≼ q` iff `#p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. Proper prefix: `p ≺ q` iff `p ≼ q ∧ p ≠ q`.
- *Derived postcondition:* `p ≺ q ⟹ #p < #q` (by T3).
