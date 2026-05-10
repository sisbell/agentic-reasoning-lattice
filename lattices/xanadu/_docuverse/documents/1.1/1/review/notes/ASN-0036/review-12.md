# Review of ASN-0036

## REVISE

### Issue 1: S8 uniqueness proof omits the derivation that sig(v) = #v

**ASN-0036, Span decomposition (S8 proof, singleton uniqueness)**: "v + 1 is the ordinal successor — incrementing only position d (by TA5(c) with k = 0, the successor has the same depth: #(v+1) = #v = d)"

**Problem**: TA5(c) says inc(v, 0) differs from v only at position sig(v). The proof claims this is position d (the tumbler depth). The identification sig(v) = d is the load-bearing step of the entire uniqueness argument — the j < d case depends on v+1 agreeing with v at all positions before d, which requires sig(v) = d — but the derivation is never given. Three steps are needed:

1. zeros(v) = 0 (by S8a)
2. All components nonzero: (A i : 1 ≤ i ≤ d : vᵢ ≠ 0) (from step 1)
3. sig(v) = max({i : 1 ≤ i ≤ d ∧ vᵢ ≠ 0}) = max({1, …, d}) = d (from step 2 and the definition of LastSignificantPosition, ASN-0034)

Without this, the proof jumps from "TA5(c) with k = 0" to "incrementing only position d" with an unstated intermediate premise.

**Required**: Insert the derivation sig(v) = #v from S8a before the case analysis. One sentence suffices: "Since zeros(v) = 0 (S8a), every component of v is nonzero, so sig(v) = #v = d — and TA5(c) with k = 0 therefore changes only position d."

### Issue 2: S5 status in properties table is mislabeled

**ASN-0036, Properties Introduced table**: S5 is labeled "introduced"

**Problem**: S5 is proved by explicit witness construction — for each N, the ASN constructs a state satisfying S0–S3 with sharing multiplicity exceeding N. This makes S5 a theorem (or meta-theorem about the consistency of S0–S3), not an axiom. Every other proved property in the table carries a "theorem from …" or "corollary of …" or "from …" label. Labeling S5 as "introduced" places it in the same category as S0 and S3 (axioms), obscuring the distinction between assumed and derived properties.

**Required**: Change the status to something like "consistent with S0–S3 (witness construction)" or "theorem from S0–S3" to reflect that S5 is derived, not postulated.

## OUT_OF_SCOPE

### Topic 1: V-space contiguity (gap-freedom as an arrangement invariant)

The ASN defines M(d) as a partial function but never states whether dom(M(d)) within a subspace must be a contiguous interval (no gaps in the V-position numbering). The worked example's deletion step removes positions 1.3–1.5, leaving {1.1, 1.2} — which happens to be contiguous, but the ASN doesn't discuss whether gaps are permitted in general. Nelson's "virtual byte stream" language suggests contiguity, but resolving this requires operation-level semantics (does DELETE close the gap or leave tombstones?), which this ASN correctly excludes from scope.

**Why out of scope**: Gap-freedom is an operation-level invariant — its maintenance (or absence) depends on how INSERT, DELETE, and REARRANGE modify dom(M(d)), which is deferred to a future ASN on operations.

### Topic 2: Unique maximal run decomposition

The ASN proves existence of a span decomposition (S8) via singleton runs but does not address whether a canonical decomposition with the fewest runs exists. This is already listed in the open questions. A future ASN on operations or enfilade structure would naturally establish whether adjacent compatible runs must be merged.

**Why out of scope**: Maximality is an optimization property over the decomposition, not a correctness invariant of the two-space model.

VERDICT: REVISE
