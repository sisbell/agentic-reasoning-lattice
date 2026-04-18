**T0(a) (UnboundedComponentValues).** `(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: #t' = #t ∧ t' agrees with t except t'.dᵢ > M)))`.

A tumbler is a finite sequence `t = d₁.d₂. ... .dₙ` where each `dᵢ ∈ ℕ` and `n ≥ 1`; the set T comprises all such sequences. The claim is that for every tumbler and every component position, there exists a tumbler whose value at that position exceeds any given bound — the address space within any subtree is inexhaustible.

*Proof.* We establish the universal claim by exhibiting, for arbitrary `t`, `i`, and `M`, a witness `t'` with the required properties.

Let `t = d₁.d₂. ... .dₙ` be an arbitrary member of T, let `i` satisfy `1 ≤ i ≤ n`, and let `M ∈ ℕ` be an arbitrary bound. Define

> `t' = d₁. ... .dᵢ₋₁.(M + 1).dᵢ₊₁. ... .dₙ`

— the sequence obtained from `t` by replacing its `i`-th component with `M + 1` and leaving all other components unchanged. We must verify four things.

*(i)* `t' ∈ T`. The sequence `t'` has length `n ≥ 1`, and each of its components is a natural number: for `j ≠ i`, the component `dⱼ ∈ ℕ` by hypothesis on `t`; for `j = i`, the component is `M + 1`, which belongs to ℕ since ℕ is closed under successor. Since T is the set of all finite sequences over ℕ with length ≥ 1, we have `t' ∈ T`.

*(ii)* `t'` agrees with `t` at every position `j ≠ i`. This holds by construction: the components at positions `j ≠ i` are identical to those of `t`.

*(iii)* `t'.dᵢ > M`. By construction `t'.dᵢ = M + 1`, and `M + 1 > M` for all `M ∈ ℕ`.

*(iv)* `#t' = #t`. By construction, `t'` has `n` components — the same count as `t` — since replacing the value at position `i` does not alter the length of the sequence.

Since `t`, `i`, and `M` were arbitrary, the universal claim holds. ∎

*Formal Contract:*
- *Postcondition:* For every tumbler `t ∈ T` and every component position `i` with `1 ≤ i ≤ #t`, and for every bound `M ∈ ℕ`, there exists `t' ∈ T` with `#t' = #t` that agrees with `t` at all positions except `i`, where `t'.dᵢ > M`.
- *Depends:* T0 (CarrierSetDefinition) — step (i) invokes T0's carrier characterisation — that T is the set of all finite sequences over ℕ with length ≥ 1 — to conclude `t' ∈ T` from `t'` being a length-`n` sequence with `n ≥ 1` whose components all lie in ℕ; and the length operator `#·` and component projection `·ᵢ` used throughout the construction and verification steps (i)–(iv) are the primitives that T0 introduces. NAT-closure (NatArithmeticClosureAndIdentity) — step (i) invokes the successor-closure clause `(A n ∈ ℕ :: n + 1 ∈ ℕ)` at `n = M` to conclude `M + 1 ∈ ℕ`, establishing that the replacement component at position `i` belongs to ℕ and is therefore admissible as a component of a member of T. NAT-addcompat (NatAdditionOrderAndSuccessor) — step (iii) invokes the strict successor inequality `(A n ∈ ℕ :: n < n + 1)` at `n = M` to conclude `M + 1 > M`, establishing that the constructed component `t'.dᵢ = M + 1` exceeds the given bound and therefore satisfies the postcondition's `t'.dᵢ > M` clause.
