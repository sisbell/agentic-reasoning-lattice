**S8-depth(c) (CorrespondenceRun).** A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that the arrangement preserves ordinal displacement within the run:

`(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`

At `k = 0` this reduces to the base case `Σ.M(d)(v) = a`. Each subsequent `k` increments both the V-ordinal and the I-ordinal by the same amount — each step forward in V-stream corresponds to the same step forward in I-stream. The notation `v + k` and `a + k` follows from S8-depth(b) (OrdinalDisplacementExtension).

*Formal Contract:*
- *Precondition:* `v ∈ dom(Σ.M(d))`, `a ∈ dom(Σ.C)`, `n ≥ 1`, all `v + k` for `0 ≤ k < n` are in `dom(Σ.M(d))`
- *Definition:* `(v, a, n)` is a correspondence run in `Σ.M(d)` iff `Σ.M(d)(v + k) = a + k` for all `0 ≤ k < n`
- *Dependencies:* S8-depth(b)
