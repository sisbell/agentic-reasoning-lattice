**ActionPoint (ActionPoint).** For w ∈ T with Pos(w), the *action point* of w is actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}).

*Derivation.* The set {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0} is a nonempty subset of ℕ: nonempty by TA-Pos, a subset of ℕ because its elements are indices with 1 ≤ i ≤ #w. By NAT-wellorder, this set has a least element, which min names. Hence actionPoint(w) is a member of the set, giving 1 ≤ actionPoint(w) ≤ #w. For any i with 1 ≤ i < actionPoint(w), wᵢ = 0: otherwise i would be a smaller member of the set, contradicting minimality. For w_{actionPoint(w)} ≥ 1: the definition gives w_{actionPoint(w)} ≠ 0; by NAT-zero, 0 ≤ w_{actionPoint(w)}; by NAT-order's definition m ≤ n ⟺ m < n ∨ m = n, this unfolds to 0 < w_{actionPoint(w)} ∨ 0 = w_{actionPoint(w)}, and w_{actionPoint(w)} ≠ 0 excludes the equality, leaving 0 < w_{actionPoint(w)}. NAT-discrete's forward direction m < n ⟹ m + 1 ≤ n at m = 0, n = w_{actionPoint(w)} yields 0 + 1 ≤ w_{actionPoint(w)}. To rewrite this via NAT-closure's additive identity (A n ∈ ℕ :: 0 + n = n) at n = 1, we first establish 1 ∈ ℕ: NAT-zero supplies 0 ∈ ℕ, and NAT-closure's successor closure (A n ∈ ℕ :: n + 1 ∈ ℕ) at n = 0 yields 0 + 1 ∈ ℕ, which is 1 ∈ ℕ since 1 denotes 0 + 1. The additive identity at n = 1 then gives 0 + 1 = 1, rewriting 0 + 1 ≤ w_{actionPoint(w)} to 1 ≤ w_{actionPoint(w)}. ∎

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
  - NAT-closure (NatArithmeticClosureAndIdentity) — successor closure `(A n ∈ ℕ :: n + 1 ∈ ℕ)` at n = 0 yielding 1 ∈ ℕ, and additive identity 0 + 1 = 1.
- *Postconditions:* 1 ≤ actionPoint(w) ≤ #w; wᵢ = 0 for all 1 ≤ i < actionPoint(w); w_{actionPoint(w)} ≥ 1
