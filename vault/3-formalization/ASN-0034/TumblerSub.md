**TumblerSub (TumblerSub).** Given two tumblers `a` (minuend) and `w` (subtrahend), compute their component-wise difference at the first point of zero-padded divergence. The primary downstream use is computing displacements between positions — given positions `a` and `b` with `b ≥ a`, the subtraction `b ⊖ a` yields the component-wise difference from `a` to `b`. This difference is a broader object than a displacement consumable by TumblerAdd: when `a` is a proper sequence-prefix of `b`, the action point of `b ⊖ a` satisfies `actionPoint(b ⊖ a) = zpd(b, a) ≥ #a + 1 > #a`, violating TumblerAdd's precondition `actionPoint(w) ≤ #a`. A second obstruction is independent of the prefix case: when `#a > #b`, the subtraction produces `#(b ⊖ a) = max(#a, #b) = #a`, and TumblerAdd's result-length identity gives `#(a ⊕ (b ⊖ a)) = #a > #b`, so `a ⊕ (b ⊖ a) ≠ b` by T3 — the round-trip fails on length alone even when the zpd constraint is satisfied. The roundtrip `a ⊕ (b ⊖ a) = b` therefore requires two independently necessary constraints: `zpd(b, a) ≤ #a` (ensuring TumblerAdd's precondition) and `#a ≤ #b` (ensuring the result length equals `#b`) — the conjunction established by D0. When the operands have different lengths, we conceptually zero-pad the shorter to the length of the longer — writing `aᵢ = 0` for `i > #a` and `wᵢ = 0` for `i > #w` — and use these padded values throughout the procedure. When the zero-padded sequences agree at every position (no divergence exists), the result is the zero tumbler of length `max(#a, #w)`: `a ⊖ w = [0, ..., 0]`. Otherwise, `zpd(a, w)` is defined (ZPD) — write `k = zpd(a, w)` for the first position at which the padded sequences disagree. The result is:

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (subtract at the divergence point)
         ⎩ aᵢ           if i > k        (copy from minuend, zero-padded)
```

The result has length `max(#a, #w)`.

**Precondition:** `a ≥ w` (T1). We prove that when `zpd(a, w)` is defined, this entails `aₖ > wₖ` at `k = zpd(a, w)`. Since zpd is defined, `a` and `w` are not zero-padded-equal (ZPD), so in particular `a ≠ w`; combined with `a ≥ w`, this yields `w < a` (T1). Two Divergence cases arise for the pair `(w, a)` with `w ≠ a`:

  (i) Component divergence at position `k ≤ min(#w, #a)` with `wₖ ≠ aₖ`. The ZPD–Divergence relationship (ZPD) gives `zpd(a, w) = divergence(a, w) = k`. Since `w < a` via T1 case (i), `wₖ < aₖ`, whence `aₖ > wₖ`.

  (ii) Prefix divergence — `w` is a proper prefix of `a` (the direction forced by `w < a` via T1 case (ii)), so `#w < #a` and `wᵢ = aᵢ` for all `1 ≤ i ≤ #w`. The padded extension sets `wₖ = 0` for `k > #w`. Since zpd is defined, the longer operand `a` has some nonzero component beyond `#w`; at `k = zpd(a, w)`, `aₖ ≠ 0 = wₖ`, so `aₖ > 0 = wₖ`.

In both cases `aₖ > wₖ` at `k = zpd(a, w)`. When zpd is undefined, no subtraction at the divergence point occurs — the constructive definition produces the zero tumbler — and the precondition holds vacuously.  ∎

Each component of the result is a natural number: for `i < k`, `rᵢ = 0 ∈ ℕ`; at the divergence point, `rₖ = aₖ − wₖ ∈ ℕ` since `a ≥ w` entails `aₖ > wₖ` at the zpd point (proved above); for `i > k`, `rᵢ` is the zero-padded value of `a`, which is either `aᵢ ∈ ℕ` (when `i ≤ #a`) or `0 ∈ ℕ` (when `i > #a`). In the equal case (no divergence), every component is `0 ∈ ℕ`. The result is therefore a finite sequence over ℕ with length `max(#a, #w) ≥ 1` — since `a, w ∈ T` requires `#a ≥ 1` and `#w ≥ 1` — hence **`a ⊖ w ∈ T`** by T0.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, a ≥ w (T1). Consequence: when zpd(a, w) is defined, aₖ > wₖ at k = zpd(a, w).
- *Depends:* T0 (CarrierSetDefinition) — membership `a ⊖ w ∈ T` is concluded via T0's characterisation of T as finite sequences over ℕ with length ≥ 1. T1 (LexicographicOrder) — the precondition `a ≥ w` is a T1 ordering; the precondition consequence derives `w < a` from `a ≥ w ∧ a ≠ w` via T1 trichotomy. Divergence (Divergence) — the precondition consequence proceeds by case analysis on Divergence's two cases for the pair `(w, a)`. ZPD (ZPD) — defines `zpd(a, w)` and supplies the ZPD–Divergence relationship identifying `zpd(a, w) = divergence(a, w) = k` in case (i).
- *Definition:* a ⊖ w computed by case analysis on k = zpd(a, w) (ZPD), all component references using zero-padded values (aᵢ = 0 for i > #a, wᵢ = 0 for i > #w); rᵢ = 0 for i < k, rₖ = aₖ − wₖ, rᵢ = aᵢ (zero-padded) for i > k; when zpd(a, w) is undefined, a ⊖ w = [0, …, 0]; #(a ⊖ w) = max(#a, #w)
- *Postconditions:* a ⊖ w ∈ T, #(a ⊖ w) = max(#a, #w)
