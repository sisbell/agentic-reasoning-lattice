**TumblerSub (TumblerSub).** Given two tumblers `a` (minuend) and `w` (subtrahend), compute their component-wise difference at the first point of zero-padded divergence. The primary downstream use is computing displacements between positions — given positions `a` and `b`, the subtraction `b ⊖ a` yields the displacement from `a` to `b` (see D0). When the operands have different lengths, we conceptually zero-pad the shorter to the length of the longer — writing `aᵢ = 0` for `i > #a` and `wᵢ = 0` for `i > #w` — and use these padded values throughout the procedure. When the zero-padded sequences agree at every position (no divergence exists), the result is the zero tumbler of length `max(#a, #w)`: `a ⊖ w = [0, ..., 0]`. Otherwise, `zpd(a, w)` is defined (ZPD) — write `k = zpd(a, w)` for the first position at which the padded sequences disagree. The result is:

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (subtract at the divergence point)
         ⎩ aᵢ           if i > k        (copy from minuend, zero-padded)
```

The result has length `max(#a, #w)`.

Each component of the result is a natural number: for `i < k`, `rᵢ = 0 ∈ ℕ`; at the divergence point, `rₖ = aₖ − wₖ ∈ ℕ` since the precondition `a ≥ w` ensures `aₖ ≥ wₖ`; for `i > k`, `rᵢ` is the zero-padded value of `a`, which is either `aᵢ ∈ ℕ` (when `i ≤ #a`) or `0 ∈ ℕ` (when `i > #a`). In the equal case (no divergence), every component is `0 ∈ ℕ`. The result is therefore a finite sequence over ℕ with length `max(#a, #w) ≥ 1` — since `a, w ∈ T` requires `#a ≥ 1` and `#w ≥ 1` — hence **`a ⊖ w ∈ T`** by T0.

**Precondition:** `a ≥ w` — when `a ≠ w`, two cases arise. If `zpd(a, w)` is defined (ZPD), then `aₖ ≥ wₖ` at `k = zpd(a, w)`. If `zpd(a, w)` is undefined (the operands are zero-padded-equal), the condition holds vacuously — the constructive definition produces the zero tumbler without any subtraction.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, a ≥ w (when a ≠ w: if zpd(a, w) is defined (ZPD), aₖ ≥ wₖ at k = zpd(a, w); if zpd(a, w) is undefined, the condition holds vacuously)
- *Definition:* a ⊖ w computed by case analysis on k = zpd(a, w) (ZPD), all component references using zero-padded values (aᵢ = 0 for i > #a, wᵢ = 0 for i > #w); rᵢ = 0 for i < k, rₖ = aₖ − wₖ, rᵢ = aᵢ (zero-padded) for i > k; when zpd(a, w) is undefined, a ⊖ w = [0, …, 0]; #(a ⊖ w) = max(#a, #w)
- *Postconditions:* a ⊖ w ∈ T, #(a ⊖ w) = max(#a, #w)
