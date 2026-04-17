## Tumbler arithmetic

We now turn to the arithmetic operations. The system requires operations that advance a position by a displacement (for computing span endpoints and shifting positions) and that recover the displacement between two positions (for computing span widths). These operations — tumbler addition (⊕, constructed in TumblerAdd) and subtraction (⊖, constructed in TumblerSub — forward reference, § Tumbler subtraction below) — are not arithmetic on numbers but position-advance operations in a hierarchical address space.

A displacement `w` is a tumbler whose leading zeros say "stay at these hierarchical levels" and whose first nonzero component says "advance here." Components after the advance point describe the structure of the landing position within the target region.

### Definition of ⊕

Tumbler addition is not arithmetic addition — it is a **position-advance operation**: given a start position `a` and a displacement `w`, compute where you land. The displacement encodes both the distance and the hierarchical level at which the advance occurs.

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

**TumblerAdd (TumblerAdd).** Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `a, w ∈ T` and `Pos(w)`. By ActionPoint, the precondition `Pos(w)` yields a well-defined action point `k = actionPoint(w)` — the least index with a nonzero component — satisfying `1 ≤ k ≤ n` and `wₖ ≥ 1`. Require `k ≤ m`: the action point must fall within the start position's length.

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

The result `a ⊕ w = [r₁, ..., rₚ]` has length `p = (k - 1) + 1 + (n - k) = n = #w`. Since `w ∈ T` requires `n ≥ 1`, the result has at least one component. We record this as the *result-length identity*: **`#(a ⊕ w) = #w`** — the length of the sum is determined entirely by the displacement, not the start position.

Each component of the result is a natural number: for `i < k`, `rᵢ = aᵢ ∈ ℕ` since `a ∈ T` and `k ≤ m` ensures position `i` exists within `a`; at the action point, `rₖ = aₖ + wₖ ∈ ℕ` by closure of ℕ under addition; for `i > k`, `rᵢ = wᵢ ∈ ℕ` since `w ∈ T`. The result is therefore a finite sequence over ℕ with length ≥ 1, hence **`a ⊕ w ∈ T`** by T0.

The construction also yields strict advancement. Since `k` is the first nonzero component of `w`, we have `wₖ ≥ 1`, so `rₖ = aₖ + wₖ ≥ aₖ + 1 > aₖ`. For all `i` with `1 ≤ i < k`, `rᵢ = aᵢ` by the construction. The precondition `k ≤ m` gives `k ≤ #a`, and the result-length identity gives `k ≤ n = #(a ⊕ w)`, so `k ≤ min(#a, #(a ⊕ w))` and both tumblers have a component at position `k`. T1 case (i) with divergence position `k` — agreement on positions `1, ..., k - 1` and strict inequality `aₖ < rₖ` — yields `a < a ⊕ w`. We record this as the *ordering guarantee*: **`a ⊕ w > a`** — tumbler addition strictly advances the start position.

The construction also yields dominance over the displacement. Since `#(a ⊕ w) = #w` (result-length identity), the T1 comparison of `a ⊕ w` and `w` reduces to finding the first position where `rᵢ ≠ wᵢ`. For `i < k`, `rᵢ = aᵢ` and `wᵢ = 0` (by definition of action point); if some `aⱼ > 0` for `j < k`, the least such `j` is a divergence point with `rⱼ > wⱼ`, so T1 case (i) gives `r > w`. If instead `aᵢ = 0` for all `i < k`, then at position `k` we have `rₖ = aₖ + wₖ` and `wₖ > 0`; when `aₖ > 0`, `rₖ > wₖ` and T1 case (i) again gives `r > w`; when `aₖ = 0`, `rₖ = wₖ`; combined with `rᵢ = aᵢ = 0 = wᵢ` for `i < k` and `rᵢ = wᵢ` for `i > k`, every component agrees, and `#r = #w` by the result-length identity, so `r = w` by T3, hence `r ≥ w`. In every case: **`a ⊕ w ≥ w`** — the result of tumbler addition dominates the displacement in T1 ordering.

These four results are load-bearing for subsequent properties that depend on TumblerAdd.

Three properties of this definition require explicit statement:

**No carry propagation:** The sum `aₖ + wₖ` at the action point is a single natural-number addition. There is no carry into position `k - 1`. This is why the operation is fast — constant time regardless of tumbler length.

**Tail replacement, not tail addition:** Components after the action point come entirely from `w`. The start position's components at positions `k + 1, ..., m` are discarded. `a ⊕ w` does not add corresponding components pairwise — it replaces the start's sub-structure with the displacement's sub-structure below the action point.

**The many-to-one property:** Because trailing components of `a` are discarded, distinct start positions can produce the same result:

```
[1, 1] ⊕ [0, 2]       = [1, 3]
[1, 1, 5] ⊕ [0, 2]    = [1, 3]
[1, 1, 999] ⊕ [0, 2]  = [1, 3]
```

This is correct and intentional: advancing to "the beginning of the next chapter" lands at the same place regardless of where you were within the current chapter. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, Pos(w) (PositiveTumbler), actionPoint(w) ≤ #a (ActionPoint)
- *Definition:* k = actionPoint(w) (ActionPoint); rᵢ = aᵢ if i < k; rₖ = aₖ + wₖ; rᵢ = wᵢ if i > k
- *Depends:* T0 (CarrierSetDefinition) — membership `a ⊕ w ∈ T` is concluded via T0's characterisation of T as finite sequences over ℕ with length ≥ 1. ActionPoint (ActionPoint) — supplies `k = actionPoint(w)` with bounds `1 ≤ k ≤ n`, the zeros-below-action-point fact `wᵢ = 0 for i < actionPoint(w)`, and the minimum-nonzero value `wₖ ≥ 1`; the dominance proof `a ⊕ w ≥ w` uses the zeros-below-k fact to license both the divergence case (`wⱼ = 0 < aⱼ = rⱼ` at the least `j < k` with `aⱼ > 0`) and the equality sub-case (`rᵢ = aᵢ = 0 = wᵢ` for `i < k` when `aᵢ = 0` throughout). PositiveTumbler (PositiveTumbler) — defines the predicate `Pos(w)` used in the precondition. T1 (LexicographicOrder) — both ordering postconditions invoke T1 case (i) at the first divergence position. T3 (CanonicalRepresentation) — the equality sub-case of `a ⊕ w ≥ w` concludes `r = w` from component-wise agreement and equal length.
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w, a ⊕ w > a (T1), a ⊕ w ≥ w (T1, T3)
