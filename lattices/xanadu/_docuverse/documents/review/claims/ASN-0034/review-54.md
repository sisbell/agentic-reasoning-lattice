# Cone Review — ASN-0034/T10a-N (cycle 1)

*2026-04-15 19:17*

I read the entire ASN as a system, tracing every definition through its uses, every precondition chain from caller to callee, and every case analysis for exhaustiveness. The proofs are detailed and correct. The cross-property chains — Prefix→T1, T1→TA5(a), TA5(b,d)→T10a-N, Prefix→T10, T10a-N→T10 — are clean. Definitions are used consistently throughout.

One finding:

### TA5 formal contract for k=0: trailing-position invariant lacks a quantified formula

**Foundation**: N/A (foundation ASN)
**ASN**: TA5 (HierarchicalIncrement), formal contract postconditions (b) and (c) for k=0

> (b) When `k = 0`: `(A i : 1 ≤ i < sig(t) : t'ᵢ = tᵢ)`.
> (c) When `k = 0`: `#t' = #t`, modification only at `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`.

**Issue**: For k=0, postcondition (b) quantifies agreement at positions `1..sig(t)−1`, and (c) specifies the value at position `sig(t)`. Positions `sig(t)+1..#t` — which exist whenever `sig(t) < #t` (trailing zeros) — are constrained only by the natural-language phrase "modification only at sig(t)" in (c). The construction proves `t'ᵢ = tᵢ` for all `i ≠ sig(t)`, but the formal contract does not export this as a quantified formula.

The gap is starkest when `sig(t) = 1` and `#t > 1` (e.g., `t = (5,0,0)`): postcondition (b) is vacuously true over the empty range `1 ≤ i < 1`, and the informal phrase in (c) carries the entire characterization of unchanged positions.

Contrast with k>0, where the contract is complete: (b) covers `1..#t`, (d) covers `#t+1..#t+k-1` and `#t+k` — every position of `t'` has a quantified specification.

No property within this ASN depends on the missing quantification (T10a-N uses k=1; TA5(a) uses only the divergence at `sig(t)`), so the gap is latent. But the precondition of TA5 is `t ∈ T`, not validity, and the contract is the exported interface for downstream consumers.

**What needs resolving**: The "modification only at sig(t)" claim needs a quantified formula — either extend (b) to `(A i : 1 ≤ i ≤ #t ∧ i ≠ sig(t) : t'ᵢ = tᵢ)`, which would subsume the current (b), or add an explicit postcondition for `(A i : sig(t) < i ≤ #t : t'ᵢ = tᵢ)`. For valid addresses where `sig(t) = #t` (by TA5-SigValid) the range is empty and the gap vanishes, but the general contract should not depend on that.

## Result

Cone converged after 2 cycles.

*Elapsed: 1645s*
