### Constructive definition of ⊕ and ⊖

The axiomatic properties above state what `⊕` and `⊖` must satisfy. We now give a constructive definition that shows how they work. Tumbler addition is not arithmetic addition — it is a **position-advance operation**: given a start position `a` and a displacement `w`, compute where you land. The displacement encodes both the distance and the hierarchical level at which the advance occurs.

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

**TumblerAdd (TumblerAdd).** Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `a, w ∈ T` and `w > 0`. Define the *action point* of `w` as `k = min{i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0}` — the index of the first nonzero component. By PositiveTumbler, the precondition `w > 0` means `(E i : 1 ≤ i ≤ n : wᵢ ≠ 0)` — at least one component of `w` is nonzero — so the set `{i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0}` is non-empty and `k` is well-defined. Require `k ≤ m`: the action point must fall within the start position's length.

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

The result `a ⊕ w = [r₁, ..., rₚ]` has length `p = (k - 1) + 1 + (n - k) = n = #w`. Since `w ∈ T` requires `n ≥ 1`, the result has at least one component. We record this as the *result-length identity*: **`#(a ⊕ w) = #w`** — the length of the sum is determined entirely by the displacement, not the start position.

Each component of the result is a natural number: for `i < k`, `rᵢ = aᵢ ∈ ℕ` since `a ∈ T` and `k ≤ m` ensures position `i` exists within `a`; at the action point, `rₖ = aₖ + wₖ ∈ ℕ` by closure of ℕ under addition; for `i > k`, `rᵢ = wᵢ ∈ ℕ` since `w ∈ T`. The result is therefore a finite sequence over ℕ with length ≥ 1, hence **`a ⊕ w ∈ T`** by T0.

These two identities are load-bearing for subsequent properties that depend on TumblerAdd.

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
- *Preconditions:* a ∈ T, w ∈ T, w > 0, actionPoint(w) ≤ #a
- *Definition:* k = min{i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0}; rᵢ = aᵢ if i < k; rₖ = aₖ + wₖ; rᵢ = wᵢ if i > k
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w
