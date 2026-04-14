**TumblerSub (TumblerSub).** Given two tumblers `a` (minuend) and `w` (subtrahend), compute their component-wise difference at the first point of zero-padded divergence. The primary downstream use is computing displacements between positions — given positions `a` and `b`, the subtraction `b ⊖ a` yields the displacement from `a` to `b` (see D0). When the operands have different lengths, we conceptually zero-pad the shorter to the length of the longer — writing `aᵢ = 0` for `i > #a` and `wᵢ = 0` for `i > #w` — and use these padded values throughout the procedure. When the zero-padded sequences agree at every position (no divergence exists), the result is the zero tumbler of length `max(#a, #w)`: `a ⊖ w = [0, ..., 0]`. Otherwise, let `k` — the *zero-padded divergence* of `a` and `w`, written `zpd(a, w)` — be the first position at which the padded sequences disagree. This concept is distinct from the formal Divergence: when one operand is a proper prefix of the other, `divergence` reports `min(#a, #w) + 1` at the prefix boundary (case (ii)), whereas `zpd` scans past it to the first position where the padded values actually differ. The result is:

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (subtract at the divergence point)
         ⎩ aᵢ           if i > k        (copy from minuend, zero-padded)
```

The result has length `max(#a, #w)`.

**Precondition:** `a ≥ w` — when `a ≠ w`, at the divergence point (after zero-padding) `aₖ ≥ wₖ`.

*Formal Contract:*
- *Preconditions:* a ≥ w (when a ≠ w, at the zero-padded divergence k = zpd(a, w), aₖ ≥ wₖ)
- *Definition:* a ⊖ w computed by case analysis on k = zpd(a, w), all component references using zero-padded values (aᵢ = 0 for i > #a, wᵢ = 0 for i > #w); rᵢ = 0 for i < k, rₖ = aₖ − wₖ, rᵢ = aᵢ (zero-padded) for i > k; when no divergence exists, a ⊖ w = [0, …, 0]; #(a ⊖ w) = max(#a, #w)
