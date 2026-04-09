**Definition (Prefix).** The prefix relation on tumblers: `p ≼ q` iff `#p ≤ #q ∧ (A i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. A proper prefix `p ≺ q` requires `p ≼ q` with `p ≠ q`, entailing `#p < #q`.

*Formal Contract:*
- *Definition:* `p ≼ q` iff `#p ≤ #q ∧ (A i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. Proper prefix: `p ≺ q` iff `p ≼ q ∧ p ≠ q`.
