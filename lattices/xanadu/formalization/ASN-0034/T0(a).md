**T0(a) (UnboundedComponentValues).** `(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: #t' = #t ∧ t' agrees with t except t'.dᵢ > M)))`.

For every tumbler and every component position, there exists a tumbler whose value at that position exceeds any given bound.

*Proof.* Let `t = d₁.d₂. ... .dₙ` be an arbitrary member of T, let `i` satisfy `1 ≤ i ≤ n`, and let `M ∈ ℕ` be an arbitrary bound. Define

> `t' = d₁. ... .dᵢ₋₁.(M + 1).dᵢ₊₁. ... .dₙ`

— the sequence obtained from `t` by replacing its `i`-th component with `M + 1`.

*(i)* `t' ∈ T`. The sequence `t'` has length `n ≥ 1`; for `j ≠ i`, `dⱼ ∈ ℕ` by hypothesis; for `j = i`, `M + 1 ∈ ℕ` by successor-closure of ℕ. Hence `t' ∈ T`.

*(ii)* `t'` agrees with `t` at every position `j ≠ i`, by construction.

*(iii)* `t'.dᵢ > M`. By construction `t'.dᵢ = M + 1`, and `M + 1 > M`.

*(iv)* `#t' = #t`. Replacing a component does not alter the sequence length. ∎

*Formal Contract:*
- *Postcondition:* For every tumbler `t ∈ T` and every component position `i` with `1 ≤ i ≤ #t`, and for every bound `M ∈ ℕ`, there exists `t' ∈ T` with `#t' = #t` that agrees with `t` at all positions except `i`, where `t'.dᵢ > M`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier characterisation of T, length operator `#·`, component projection `·ᵢ`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — successor-closure `(A n ∈ ℕ :: n + 1 ∈ ℕ)`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `(A n ∈ ℕ :: n < n + 1)`.
