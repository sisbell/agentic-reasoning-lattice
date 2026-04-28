Addition on ℕ is non-strictly monotone with respect to order on either side:
if `p ≤ n` then `m + p ≤ m + n` (left) and `p + m ≤ n + m` (right) for all
`m`. Both forms are stated as axiom clauses so proofs that add a fixed
summand on either side need not tacitly assume commutativity — GlobalUniqueness
Case 5's sub-case `k'₁ < k'₂` uses both placements, left to lift `k'₁ ≤ k'₂` to
`#p₁ + k'₁ ≤ #p₁ + k'₂` and right to lift `#p₁ ≤ #p₂` to
`#p₁ + k'₂ ≤ #p₂ + k'₂`. The clauses deliver only non-strict `≤`; promoting
`#p₁ < #p₂` to the strict `#p₁ + k'₂ < #p₂ + k'₂` requires combining NAT-addcompat
with NAT-cancel (to rule out the equality `#p₁ + k'₂ = #p₂ + k'₂`) and NAT-order
(to weaken `<` to `≤` and to re-strengthen `≤` with non-equality back to
`<`). Additionally, every natural number is strictly less than its
successor: `n < n + 1`. The axiom body cites the non-strict `≤` defined in
NAT-order and the addition/`1`-constants supplied by NAT-closure, so both
foundations appear in the Depends slot.
