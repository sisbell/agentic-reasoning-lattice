**ActionPoint (ActionPoint).** For w ∈ T with Pos(w), the *action point* of w, written actionPoint(w), is the unique m ∈ S such that (A n ∈ S :: m ≤ n), where S = {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}.

*Derivation.* The set S = {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0} is a nonempty subset of ℕ: nonempty by TA-Pos, a subset of ℕ because its elements are indices with 1 ≤ i ≤ #w. By NAT-wellorder, there exists m ∈ S with (A n ∈ S :: m ≤ n). Such m is unique: if m₁ and m₂ both satisfy the clause, then m₁ ≤ m₂ and m₂ ≤ m₁, and NAT-order's trichotomy excludes both m₁ < m₂ (which would force the disjunct m₂ < m₁ ∨ m₂ = m₁ in m₂ ≤ m₁ to land on m₂ < m₁, violating trichotomy's exclusivity against m₁ < m₂) and m₂ < m₁ (symmetrically), leaving m₁ = m₂. So actionPoint(w) names this element unambiguously, and actionPoint(w) ∈ S, giving 1 ≤ actionPoint(w) ≤ #w. For any i with 1 ≤ i < actionPoint(w), wᵢ = 0: otherwise i would be a member of S with i < actionPoint(w), contradicting (A n ∈ S :: actionPoint(w) ≤ n). For 1 ≤ w_{actionPoint(w)}: membership of actionPoint(w) in S gives w_{actionPoint(w)} ≠ 0; by NAT-zero, 0 ≤ w_{actionPoint(w)}; by NAT-order's definition m ≤ n ⟺ m < n ∨ m = n, this unfolds to 0 < w_{actionPoint(w)} ∨ 0 = w_{actionPoint(w)}, and w_{actionPoint(w)} ≠ 0 excludes the equality, leaving 0 < w_{actionPoint(w)}. NAT-discrete's forward direction m < n ⟹ m + 1 ≤ n at m = 0, n = w_{actionPoint(w)} yields 0 + 1 ≤ w_{actionPoint(w)}. NAT-closure posits 1 ∈ ℕ directly, licensing its additive identity (A n ∈ ℕ :: 0 + n = n) to be instantiated at n = 1; this gives the equality 0 + 1 = 1, and rewriting 0 + 1 ≤ w_{actionPoint(w)} by it yields 1 ≤ w_{actionPoint(w)}. ∎

*Formal Contract:*
- *Preconditions:* w ∈ T, Pos(w)
- *Definition:* actionPoint(w) is the unique m ∈ S with (A n ∈ S :: m ≤ n), where S = {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies T, #w, and component projection wᵢ.
  - TA-Pos (PositiveTumbler) — supplies Pos(w) and the existential making S nonempty.
  - NAT-wellorder (NatWellOrdering) — least-element principle giving existence of m ∈ S with (A n ∈ S :: m ≤ n).
  - NAT-zero (NatZeroMinimum) — supplies 0 ≤ w_{actionPoint(w)} and 0 ∈ ℕ.
  - NAT-order (NatStrictTotalOrder) — definition of ≤ as `m ≤ n ⟺ m < n ∨ m = n`; trichotomy, used to secure uniqueness of the least element of S.
  - NAT-discrete (NatDiscreteness) — forward direction m < n ⟹ m + 1 ≤ n.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` directly and the additive identity `(A n ∈ ℕ :: 0 + n = n)`, whose instantiation at n = 1 gives the equality 0 + 1 = 1 used to rewrite.
- *Postconditions:* 1 ≤ actionPoint(w) ≤ #w; wᵢ = 0 for all 1 ≤ i < actionPoint(w); 1 ≤ w_{actionPoint(w)}
