# Review of ASN-0102

This is a thorough, multiply-refined operation spec. The arithmetic in all five worked examples checks out, the tiling argument in X16 is correct across the full range `1 ≤ p ≤ n_S+1`, the wp(COPY, S3★) reduction is non-trivial and properly discharged, and every conjunct of ExtendedReachableStateInvariants is accounted for. The cross-ASN references are all to foundation ASNs, so they are permitted. My findings are confined to residual anti-bloat and one citation slip.

## REVISE

### Issue 1: Superfluous restatement in X16's cross-subspace disjointness
**ASN-0102, X16 (PostStateDensity)**: "…so they disagree at position 1 and are distinct tumblers by T3 (CanonicalRepresentation, ASN-0034) — *equivalently, separated by T1 at the first divergence position.*"
**Problem**: The disjointness/S2 conclusion needs only *distinctness*, which T3 already delivers. The trailing "equivalently, separated by T1" clause restates the same conclusion in a second vocabulary and advances no step of the argument — exactly the "two clauses saying the same thing in different words" pattern the anti-bloat pass is meant to catch.
**Required**: Delete the "— equivalently, separated by T1 at the first divergence position" clause.

### Issue 2: Spurious citation in X14
**ASN-0102, X14**: "Every member of A is mapped at a fresh copied position v+c (P3, PC3), so A ⊆ ran_{s_C}(Σ'.M(d))…"
**Problem**: P3 (ArrangementMutabilityOnly — M is the only contractible/rewritable component) does not support the claim that each copied address is mapped at a content-subspace position. The membership in `ran_{s_C}` follows from the effect clause (the position is bound by COPY) together with PC3 (the position is subspace `s_C`). P3 is unrelated here.
**Required**: Drop "P3" — cite the effect clause and PC3 only.

## OUT_OF_SCOPE

### Topic 1: Discoverability/identity of copied content under later displacement, unreachable origin, time-varying views
**Why out of scope**: The four Open Questions concern link-projection displacement, replication, and version-derivation semantics — these are correctly deferred and explicitly listed in the scope exclusions, not gaps in COPY itself.

VERDICT: REVISE
