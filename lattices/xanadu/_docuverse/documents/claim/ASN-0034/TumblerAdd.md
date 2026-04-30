## Tumbler arithmetic

The system requires an operation that advances a position by a displacement — for computing span endpoints and shifting positions. This operation is tumbler addition (⊕), constructed here as TumblerAdd. It is not arithmetic on numbers but a position-advance operation in a hierarchical address space. Its inverse — tumbler subtraction (⊖), which recovers the displacement between two positions — is constructed below as TumblerSub.

A displacement `w` is a tumbler whose leading zeros say "stay at these hierarchical levels" and whose first nonzero component says "advance here." Components after the advance point describe the structure of the landing position within the target region.

### Definition of ⊕

Tumbler addition is a **position-advance operation**: given a start position `a` and a displacement `w`, compute where you land. The displacement encodes both the distance and the hierarchical level at which the advance occurs.

```
START:  1.0.3.0.2.0.1.777
  DIF:  0.0.0.0.0.0.0.300
        ──────────────────
AFTER:  1.0.3.0.2.0.1.1077
```

Reading the displacement `[0,0,0,0,0,0,0,300]`: seven leading zeros mean "same server, same account, same document, same subspace." Component 8 is 300: "advance 300 elements." No trailing components: the landing position has no further sub-structure.

A displacement that acts at a higher level:

```
START:  1.0.3.0.2.0.1.777
  DIF:  0.0.0.0.3.0.1.1
        ──────────────────
AFTER:  1.0.3.0.5.0.1.1
```

Reading `[0,0,0,0,3,0,1,1]`: four leading zeros mean "same server, same account." Component 5 is 3: "advance 3 documents." Trailing `[0,1,1]`: "land at element 1.1 in the target document." The start position's element field `[1,777]` is replaced by the displacement's trailing structure `[1,1]`.

**TumblerAdd (TumblerAdd).** Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `a, w ∈ T` and `Pos(w)`. By ActionPoint, `k = actionPoint(w)` satisfies `1 ≤ k ≤ n` and `wₖ ≥ 1`. Require `k ≤ m`.

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

The result `a ⊕ w = [r₁, ..., rₚ]` has length `p = (k - 1) + 1 + (n - k) = n = #w`, where `k - 1 ∈ ℕ` and `n - k ∈ ℕ` are well-defined by NAT-sub's conditional closure under `k ≥ 1` and `n ≥ k`, and the collapses `(k - 1) + 1 = k` and `k + (n - k) = n` are NAT-sub's right- and left-inverse characterisations. Since `n ≥ 1`, the result has at least one component. *Result-length identity:* **`#(a ⊕ w) = #w`**.

Each component of the result is a natural number: for `i < k`, `rᵢ = aᵢ ∈ ℕ` since `a ∈ T` and `k ≤ m`; at the action point, `rₖ = aₖ + wₖ ∈ ℕ` by NAT-closure; for `i > k`, `rᵢ = wᵢ ∈ ℕ`. The map `i ↦ rᵢ` therefore assigns a natural number to each `i ∈ {j ∈ ℕ : 1 ≤ j ≤ p}`, and `p = n ≥ 1`; T0's comprehension clause, instantiated at length `p` and component map `r`, supplies a tumbler in T whose length is `p` and whose `i`-th component is `rᵢ`. Therefore **`a ⊕ w ∈ T`**.

*Strict advancement.* From `wₖ ≥ 1`, NAT-addcompat's left order-compatibility gives `aₖ + wₖ ≥ aₖ + 1`, and its strict successor inequality gives `aₖ + 1 > aₖ`. NAT-order composes these into `aₖ + wₖ > aₖ`, i.e., `rₖ > aₖ`. For `1 ≤ i < k`, `rᵢ = aᵢ`. Since `k ≤ #a` and `k ≤ #(a ⊕ w) = n`, T1 case (i) at divergence position `k` yields **`a ⊕ w > a`**.

*Dominance over displacement.* Since `#(a ⊕ w) = #w`, the T1 comparison reduces to finding the first `i` where `rᵢ ≠ wᵢ`. For `i < k`, `rᵢ = aᵢ` and `wᵢ = 0`. Case split on `(∃j ∈ [1, k-1] : aⱼ > 0)`:

*Case some `aⱼ > 0` for `j < k`.* NAT-wellorder applied to `{j : 1 ≤ j < k ∧ aⱼ > 0}` supplies the least such `j`. For `1 ≤ i < j`: `aᵢ = 0` by minimality of `j`, `wᵢ = 0` by ActionPoint, `rᵢ = aᵢ`, so `rᵢ = wᵢ = 0`. At `j`: `wⱼ = 0` by ActionPoint, `rⱼ = aⱼ > 0`, so `rⱼ > wⱼ`. The bound `j ≤ #w` follows from `j < k ≤ #w` via NAT-order. T1 case (i) at `j` yields `r > w`.

*Case `aᵢ = 0` for all `i < k`.* Then `rₖ = aₖ + wₖ`. Sub-case split on `aₖ > 0 ∨ aₖ = 0` from NAT-zero + NAT-order:
- If `aₖ > 0`: NAT-addcompat's right order-compatibility lifts `0 ≤ aₖ` into `aₖ + wₖ ≥ 0 + wₖ`; NAT-closure's additive identity rewrites this as `aₖ + wₖ ≥ wₖ`; NAT-cancel's symmetric summand absorption `n + m = m ⟹ n = 0`, instantiated at `n = aₖ, m = wₖ`, rules out equality (which would force `aₖ = 0`), so NAT-order delivers `aₖ + wₖ > wₖ`, i.e., `rₖ > wₖ`. T1 case (i) at `k` yields `r > w`.
- If `aₖ = 0`: `rₖ = wₖ` (via NAT-closure's additive identity); combined with `rᵢ = 0 = wᵢ` for `i < k` and `rᵢ = wᵢ` for `i > k`, every component agrees and `#r = #w`, so `r = w` by T3.

The strict branches discharge `r > w` via T1 case (i); the equality branch discharges `r = w` via T3. Their disjunction `r > w ∨ r = w` is **`a ⊕ w ≥ w`** by T1's `≥` abbreviation `a ≥ b ≡ b < a ∨ b = a`. ∎

Three properties of this definition — characterizations of what ⊕ does rather than postconditions to discharge — require explicit statement.

**No carry propagation:** The sum `aₖ + wₖ` at the action point is a single natural-number addition. There is no carry into position `k - 1`. This is why the operation is fast — constant time regardless of tumbler length.

**Tail replacement, not tail addition:** Components after the action point come entirely from `w`. The start position's components at positions `k + 1, ..., m` are discarded. `a ⊕ w` does not add corresponding components pairwise — it replaces the start's sub-structure with the displacement's sub-structure below the action point.

**The many-to-one property:** Because trailing components of `a` are discarded, distinct start positions can produce the same result:

```
[1, 1] ⊕ [0, 2]       = [1, 3]
[1, 1, 5] ⊕ [0, 2]    = [1, 3]
[1, 1, 999] ⊕ [0, 2]  = [1, 3]
```

This is correct and intentional: advancing to "the beginning of the next chapter" lands at the same place regardless of where you were within the current chapter.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a
- *Definition:* k = actionPoint(w); rᵢ = aᵢ if i < k; rₖ = aₖ + wₖ; rᵢ = wᵢ if i > k
- *Depends:*
  - T0 (CarrierSetDefinition) — comprehension clause, instantiated at result-length `p ≥ 1` and the component map `i ↦ rᵢ` valued in ℕ, discharges `a ⊕ w ∈ T`; component projection supplies `aⱼ, aₖ ∈ ℕ` for dichotomy sites.
  - NAT-closure (NatArithmeticClosureAndIdentity) — closure of ℕ under addition at `rₖ = aₖ + wₖ`; additive identity `0 + wₖ = wₖ` in the dominance proof.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left order-compatibility and strict successor inequality for strict advancement; right order-compatibility for dominance sub-case `aₖ > 0`.
  - NAT-cancel (NatAdditionCancellation) — summand absorption symmetric form `n + m = m ⟹ n = 0`, instantiated at `n = aₖ, m = wₖ`, rules out `aₖ + wₖ = wₖ` in the dominance sub-case `aₖ > 0`.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n` at dichotomy sites.
  - NAT-order (NatStrictTotalOrder) — defining clause unfolds `≤` at dichotomy and strict-promotion sites; transitivity composes bounds.
  - NAT-wellorder (NatWellOrdering) — least element of `{j : 1 ≤ j < k ∧ aⱼ > 0}` in the divergence sub-case.
  - NAT-sub (NatPartialSubtraction) — conditional closure of `k - 1` and `n - k`; right-inverse `(m − n) + n = m` at `(k − 1) + 1 = k` and left-inverse `n + (m − n) = m` at `k + (n − k) = n` collapse the result-length identity.
  - ActionPoint (ActionPoint) — bounds `1 ≤ k ≤ #w`, zeros-below-action-point `wᵢ = 0` for `i < k`, and `wₖ ≥ 1`.
  - TA-Pos (PositiveTumbler) — the predicate `Pos(w)` in the precondition.
  - T1 (LexicographicOrder) — case (i) at the divergence position for the strict-advancement postcondition and for the strict branches of dominance; `≥` abbreviation (`a ≥ b ≡ b < a ∨ b = a`) merges the dominance proof's strict and equality branches to deliver `a ⊕ w ≥ w`.
  - T3 (CanonicalRepresentation, this ASN) — equality sub-case of dominance concludes `r = w` from component-wise agreement and equal length.
- *Forward References:*
  - TumblerSub (TumblerSub) — the inverse operation, constructed below in this ASN; TumblerAdd's correctness does not depend on it.
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w, a ⊕ w > a (T1), a ⊕ w ≥ w (T1, T3)
