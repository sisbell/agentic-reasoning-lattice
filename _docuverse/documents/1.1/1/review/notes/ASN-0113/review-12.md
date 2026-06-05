# Review of ASN-0113

## REVISE

### Issue 1: W5's forward direction does not actually follow from W4

**ASN-0113, "The extent of a single subspace" (W5, ExactnessRequiresContiguity)**: "there exists a single level-uniform span `σ` of subspace `S` at depth `m` satisfying `⟦σ⟧ ∩ VSlice(S, m) = V_S(d)` *if and only if* `V_S(d)` is contiguous in `VSlice(S, m)`. … The *forward* direction (contiguous ⟹ a single exact span exists) is W4 itself: under D-CTG★ the run is contiguous, and `ext(d, S)` exactly covers it."

**Problem**: The two halves of the W5 biconditional are proved under mismatched invariant assumptions, and the forward proof is invalid for the generality the converse demands.

- The **converse** is deliberately argued over *arbitrary, non-docuverse* configurations — its counterexample `{[S,1], [S,3]}` violates D-CTG★ and could never arise in a reachable state. The point of W5 ("an alternative implementation must not lose it") is to assert a general span-algebra fact, not merely a docuverse-restricted one.
- The **forward** direction, however, silently imports D-MIN★/D-SEQ★ by invoking `ext(d, S)`. `ext(d, S) = ([S,1,…,1], δ(n_S, m_S))` is anchored at `[S,1,…,1]`. W4's exactness holds *only because* D-SEQ★ pins `V_S(d)` to the canonical run `{[S,1,…,1,k]}`. For a contiguous run not anchored at the canonical minimum — e.g. `V_S(d) = {[S,5,3], [S,5,4]}` (contiguous in `VSlice(S,3)`, no interior gaps) — `ext(d, S)` reaches only `[S,1,3]`, so `⟦ext(d,S)⟧ ∩ VSlice(S,3) = {[S,1,1],[S,1,2]} ≠ V_S(d)`. The exact covering span is `([S,5,3], δ(2,3))`, which is *not* `ext(d, S)`.

So "the forward direction is W4 itself" is false once W5 is read at the generality its converse requires. The existence claim is still true (a contiguous run, by unboundedness of the last component via T0(a), must share components `1..m−1`, so the span from the run's actual minimum covers it exactly), but that construction is not `ext(d, S)` and is not what W4 establishes.

**Required**: Either (a) restrict W5's statement and converse to standing-invariant states (where D-MIN★ forces the canonical anchor and "W4 itself" is genuinely sufficient — but then note the converse concerns a hypothetical relaxation, not a reachable state), or (b) keep W5 general and replace "is W4 itself" with an explicit construction of the covering span from the run's *actual* minimum `min(V_S(d))` rather than `[S,1,…,1]`, proving exactness by T5 on the run's shared prefix. As written, the forward direction borrows an assumption (canonical anchor) that the converse explicitly discards.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
