### Subtraction for width computation

Let `⊖` denote tumbler subtraction: given two positions, compute the displacement between them.

**TA2 (WellDefinedSubtraction).** For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

*Proof.* We show that for all `a, w ∈ T` with `a ≥ w`, the operation `a ⊖ w` as defined by TumblerSub produces a member of `T` — a finite sequence of non-negative integers with at least one component.

By TumblerSub, subtraction zero-pads both operands to length `p = max(#a, #w)` and scans for the first position at which the padded sequences disagree. Two cases arise.

*Case 1: no divergence (zero-padded equality).* The padded sequences of `a` and `w` agree at every position. TumblerSub produces the zero tumbler `[0, ..., 0]` of length `p`. Since `#a ≥ 1` and `#w ≥ 1` (both are tumblers in T), `p ≥ 1`. Each component is `0 ∈ ℕ`. The result is a finite sequence of non-negative integers with length at least 1 — a member of T.

*Case 2: divergence at position `k`.* The padded sequences agree at all positions `i < k` and disagree at `k`. TumblerSub defines the result `r = a ⊖ w` componentwise: `rᵢ = 0` for `i < k`, `rₖ = aₖ - wₖ`, and `rᵢ = aᵢ` for `i > k` (where all component references use zero-padded values), with `#r = p`.

We verify that each region produces non-negative integer components.

*Pre-divergence* (`i < k`): `rᵢ = 0 ∈ ℕ`.

*Divergence point* (`i = k`): We must show `aₖ ≥ wₖ` (zero-padded values) so that `rₖ = aₖ - wₖ ∈ ℕ`. Since the divergence exists, the padded sequences differ, so `a` and `w` are not zero-padded-equal. If `a = w` as tumblers (by T3: same length and components), then their padded sequences are trivially identical — no divergence exists, contradicting the case hypothesis. Therefore `a ≠ w`, and combined with `a ≥ w` this gives `a > w` under T1. Two sub-cases arise from T1's definition of strict ordering.

*Sub-case (i): T1 case (i) — component divergence.* There exists a first position `j ≤ min(#a, #w)` with `aⱼ > wⱼ` and `aᵢ = wᵢ` for all `i < j`. These positions lie within both original sequences, so the zero-padded values agree with the originals. The padded sequences therefore agree before `j` and disagree at `j`, making `j` the first padded divergence: `k = j`. At position `k`, `aₖ > wₖ`, so `rₖ = aₖ - wₖ ∈ ℕ`.

*Sub-case (ii): T1 case (ii) — prefix relationship.* Here `w` is a proper prefix of `a`: `#w < #a` and `aᵢ = wᵢ` for all `i ≤ #w`. Zero-padding extends `w` with zeros at positions `#w + 1` through `p = #a`. The padded sequences agree at all positions `i ≤ #w`. The divergence `k` falls at the first position `i > #w` where `aᵢ > 0` — such a position must exist, for if `aᵢ = 0` at every `i > #w` the padded sequences would agree everywhere, contradicting the case hypothesis. At position `k`, `aₖ > 0 = wₖ` (zero-padded), so `rₖ = aₖ - 0 = aₖ ∈ ℕ`.

*Tail* (`i > k`): `rᵢ = aᵢ` (zero-padded). If `i ≤ #a`, then `aᵢ` is a component of `a ∈ T`, hence `aᵢ ∈ ℕ`. If `i > #a`, then `aᵢ = 0 ∈ ℕ` (zero-padded).

The result `r` has length `p = max(#a, #w) ≥ 1` with every component in ℕ — a member of T.

In both cases, `a ⊖ w ∈ T`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, a ≥ w
- *Postconditions:* a ⊖ w ∈ T
