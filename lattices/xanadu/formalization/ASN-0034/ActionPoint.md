**ActionPoint (ActionPoint).** For w ∈ T with Pos(w), the *action point* of w is actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}).

*Derivation.* The set {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0} is a nonempty subset of ℕ: nonempty by TA-Pos, a subset of ℕ because its elements are indices with 1 ≤ i ≤ #w. By NAT-wellorder, this set has a least element, which min names. Hence actionPoint(w) is a member of the set, giving 1 ≤ actionPoint(w) ≤ #w. For any i with 1 ≤ i < actionPoint(w), wᵢ = 0: otherwise i would be a smaller member of the set, contradicting minimality. For w_{actionPoint(w)} ≥ 1: the definition gives w_{actionPoint(w)} ≠ 0; by NAT-zero, 0 ≤ w_{actionPoint(w)}; by NAT-order's definition m ≤ n ⟺ m < n ∨ m = n, this unfolds to 0 < w_{actionPoint(w)} ∨ 0 = w_{actionPoint(w)}, and w_{actionPoint(w)} ≠ 0 excludes the equality, leaving 0 < w_{actionPoint(w)}. NAT-discrete's forward direction m < n ⟹ m + 1 ≤ n at m = 0, n = w_{actionPoint(w)} yields 0 + 1 ≤ w_{actionPoint(w)}. NAT-closure posits 1 ∈ ℕ directly, licensing its additive identity (A n ∈ ℕ :: 0 + n = n) to be instantiated at n = 1; this gives the equality 0 + 1 = 1, and rewriting 0 + 1 ≤ w_{actionPoint(w)} by it yields 1 ≤ w_{actionPoint(w)}. ∎

*Formal Contract:*
- *Preconditions:* w ∈ T, Pos(w)
- *Definition:* actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0})
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies T, #w, and component projection wᵢ.
  - TA-Pos (PositiveTumbler) — supplies Pos(w) and the existential making the set nonempty.
  - NAT-wellorder (NatWellOrdering) — least-element principle making min well-defined.
  - NAT-zero (NatZeroMinimum) — supplies 0 ≤ w_{actionPoint(w)} and 0 ∈ ℕ.
  - NAT-order (NatStrictTotalOrder) — definition of ≤ as `m ≤ n ⟺ m < n ∨ m = n`.
  - NAT-discrete (NatDiscreteness) — forward direction m < n ⟹ m + 1 ≤ n.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` directly and the additive identity `(A n ∈ ℕ :: 0 + n = n)`, whose instantiation at n = 1 gives the equality 0 + 1 = 1 used to rewrite.
- *Postconditions:* 1 ≤ actionPoint(w) ≤ #w; wᵢ = 0 for all 1 ≤ i < actionPoint(w); w_{actionPoint(w)} ≥ 1
