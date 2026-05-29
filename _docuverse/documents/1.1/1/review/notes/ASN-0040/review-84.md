# Review of ASN-0040

## REVISE

### Issue 1: S0 cites a foundation result whose precondition it does not discharge
**ASN-0040, §The sibling stream (S0 + the "Correspondence" paragraph)**: "Strict ordering (S0) needs only the inc(·, 0)-enumeration form, so it holds for any p ∈ T, d ≥ 1" — proved via "T10a.7 (EnumerationInjectivity)."
**Problem**: T10a.7's contract precondition is "Allocator A *conforming to T10a*." For arbitrary `p ∈ T, d ≥ 1` the allocator `A(p, d)` need not conform: for `d ≥ 3` the base `inc(p, d)` is not T4-valid, and for non-T4 `p` the base may fail T4 as well. The ASN itself notes conformance is supplied only "there by B6." So the cited T10a.7 does not license S0 over the full domain `p ∈ T, d ≥ 1` — only over B6-valid pairs. The claim is true, but the proof covers a strictly smaller set than the contract asserts.
**Required**: Either restrict S0's postcondition to B6-valid `(p, d)`, or prove S0 directly from TA5(a) (per-step strict increase) and T1 transitivity/irreflexivity — which is all T10a.7's own proof uses — instead of routing through the conformance-gated foundation result.

### Issue 2: B7 imports an unstated co-tree hypothesis
**ASN-0040, §Namespace disjointness (B7 proof)**: "the allocators all sit in the common allocator tree rooted at the seed... T10a.6 (DomainDisjointness) delivers [disjointness] for any two *distinct* conforming allocators."
**Problem**: B7's precondition is only that both `(p, d)` and `(p', d')` satisfy B6 — i.e. `p, p'` are T4-valid and `d, d' ∈ {1, 2}`. This does not establish that `A(p, d)` and `A(p', d')` lie in one allocator tree. T10a.6's proof routes the non-ancestor–descendant case through T10a.5, which "traces to the lowest common ancestor" — presupposing a common tree with a defined LCA. Two unrelated T4-valid parents (e.g. node `[5]` and node `[7]`) yield distinct conforming allocators with no derived common ancestor, yet B7 claims them in scope. The "common allocator tree rooted at the seed" is asserted, not derived from B6.
**Required**: Either add the co-tree membership to B7's preconditions (and justify it for the system's reachable allocators), or show that namespace injectivity + B6 alone places both allocators in a single T10a tree so that T10a.6's LCA-based case analysis applies. As written, B1 and B8 inherit this gap through their reliance on B7.

### Issue 3: Meta-prose and reviser-drift residue (anti-bloat)
**ASN-0040, §Correspondence to the allocator framework**: "Strict ordering (S0) needs only the inc(·, 0)-enumeration form, so it holds for any p ∈ T, d ≥ 1; disjointness (B7) needs full T10a-conformance, supplied there by B6."
**Problem**: This is a use-site inventory — it enumerates which downstream claim consumes which conformance level rather than advancing the correspondence's meaning. (It is also the carrier of the Issue-1 overreach.)
**Also, §Namespace disjointness (B7 proof)**: "the prefix-incomparable case that the earlier hand-written argument re-walked." This references a prior revision's proof, not the current argument — relocated/leftover meta-commentary that the precise reader must skip.
**Required**: Delete the use-site inventory sentence (fold any needed conformance qualification directly into S0 and B7). Remove the "earlier hand-written argument" clause; state the case on its own terms.

## OUT_OF_SCOPE

### Topic 1: B3 Ghost Validity as a constraint on content storage
**ASN-0040, §Ghost elements (B3)**: introduces `Occupied : T × 𝒮 → {⊤, ⊥}` and the requirement `Occupied(t, s) ⟹ t ∈ s.B`.
**Why out of scope**: Content storage and retrieval are explicitly deferred. The baptized/unbaptized distinction and the *prose* on ghost elements belong here, but the formal predicate `Occupied` and the content-permission requirement are object-level constraints on the future content-storage ASN, not properties of the baptismal state machine this ASN defines.

VERDICT: REVISE
