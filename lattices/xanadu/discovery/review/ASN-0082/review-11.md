# Review of ASN-0082

## REVISE

### Issue 1: I3-VD and I3-VP derivations assume closed-world that the postconditions do not establish

**ASN-0082, Structural preservation (I3-VD)**: "V-positions in dom(M'(d)) within subspace S fall into two regions."

**Problem**: The I3-VD derivation treats the left region (I3-L) and shifted region (I3) as an exhaustive enumeration of dom(M'(d)) ∩ subspace S. The I3-VP derivation similarly enumerates three regions as exhaustive over all of dom(M'(d)). But the five postconditions only constrain positions that *were* in dom(M(d)): I3, I3-L, and I3-X specify which pre-existing positions are retained (with possibly new keys); I3-V specifies which are removed. Positions *not* in dom(M(d)) — including unoccupied gap positions in [p, shift(p, n)) and any other position outside the pre-state domain — are unconstrained by any clause. An M'(d) satisfying all five clauses could therefore contain additional positions at arbitrary depth within subspace S, falsifying I3-VD's universal quantification `(A v₁, v₂ ∈ dom(M'(d)) : ...)`. The identical gap affects I3-VP's `(A v ∈ dom(M'(d)) : v₁ ≥ 1)`.

The ASN acknowledges that gap positions are unspecified ("the content-placement postcondition is an operation-level concern deferred to a future INSERT ASN"), but then derives I3-VD and I3-VP as if they quantify over a fully determined dom(M'(d)). This is a genuine logical gap — the derivation proves a universal statement over a domain it has not closed.

**Required**: Either:

(a) Add closure frame clauses that make the enumeration exhaustive. For subspace S: `(A v : v ∈ dom(M'(d)) ∧ subspace(v) = S : (v < p ∧ v ∈ dom(M(d))) ∨ (∃ u ∈ dom(M(d)) : subspace(u) = S ∧ u ≥ p ∧ v = shift(u, n)))`. For cross-subspace: `(A v : v ∈ dom(M'(d)) ∧ subspace(v) ≠ S : v ∈ dom(M(d)))`. With these, I3-VD and I3-VP follow as written. Note explicitly that the future INSERT ASN's content-placement postcondition extends this closed domain and must re-derive VD/VP for the complete post-state.

(b) Or weaken I3-VD and I3-VP to quantify only over positions assigned by I3, I3-L, and I3-X — not over all of dom(M'(d)). This accurately reflects what the shift postconditions can establish.

## OUT_OF_SCOPE

### Topic 1: Cross-boundary spans
**Why out of scope**: A span σ with start(σ) < p < reach(σ) straddles the insertion point — the left portion is unchanged while the right portion shifts. Handling this composes ASN-0053's S4 (split at p) with I3-S and is an operation-level concern for the future INSERT ASN, not a span displacement algebra property.

VERDICT: REVISE
