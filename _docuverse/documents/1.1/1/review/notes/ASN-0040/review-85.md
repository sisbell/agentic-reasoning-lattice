# Review of ASN-0040

## REVISE

### Issue 1: "Correspondence to the allocator framework" paragraph is unused scaffolding
**ASN-0040, §The sibling stream (Correspondence paragraph)**: "The sibling stream S(p, d) is exactly the domain of a foundation allocator (T10a, ASN-0034). … Write A(p, d) for this allocator … When (p, d) satisfies B6 … A(p, d) conforms to T10a. The correspondence situates the sibling stream within the foundation's allocator framework; the stream properties we need below (S0, B7) we nonetheless prove directly from the increment algebra…"
**Problem**: The paragraph establishes a correspondence (S(p,d) = dom(A(p,d)), conformance to T10a) and then states in the same breath that the proofs deliberately do *not* use it — S0, B7, B1, B10 all argue directly from TA5/TA5a. No downstream claim consumes A(p,d) or its T10a conformance. This is exactly the forward-reference accretion the anti-bloat classifier targets: a use-site framing left behind after the proofs were decoupled from the allocator framework, advancing no reasoning.
**Required**: Delete the paragraph, or reduce it to a single sentence noting the correspondence exists, with no conformance derivation, since nothing uses it.

### Issue 2: B7 proof opens with a defensive justification of its own method
**ASN-0040, §Namespace disjointness (B7 proof, first paragraph)**: "We argue directly from the element structure of the two streams, rather than routing through the foundation's domain-disjointness theorem. That theorem (T10a.6) would require both allocators to inhabit one allocator tree with a defined common ancestor; B6 … supplies no such common tree … so the hypothesis it needs is precisely what B6 fails to give. The direct argument needs no tree."
**Problem**: This is meta-prose explaining why a downstream theorem is *not* used — a defensive justification of proof approach, not a step of the proof. The reader must skip it to reach the actual argument ("Suppose, for contradiction, some x ∈ …"). Reviser drift around a forward reference.
**Required**: Remove the paragraph; begin the proof at the contradiction setup. The direct argument stands on its own.

### Issue 3: Max-existence well-definedness is re-derived verbatim in Bop
**ASN-0040, §The baptism operation (Bop freshness proof)**: "the maximum exists because children(s.B, p, d) is a non-empty finite subset of T (finite by B_fin, totally ordered by T1)."
**Problem**: This duplicates the NextAddress *Justification of well-definedness* ("children(B, p, d) is a non-empty finite subset of T (finite by B_fin), which T1 totally orders, so its max exists"). Two paragraphs assert the same fact in nearly identical words. The freshness argument can cite NextAddress's well-definedness rather than re-prove max-existence.
**Required**: Replace the re-derivation with a reference to NextAddress's already-established totality, keeping only the freshness-specific step (a > q for every prior child).

### Issue 4: S0 proof carries a scope-defending clause that is argument-external
**ASN-0040, §The sibling stream (S0 proof)**: "We argue directly from the per-step strict increase of the increment, requiring no T4-conformance and so covering the full domain p ∈ T, d ≥ 1."
**Problem**: The "requiring no T4-conformance and so covering the full domain" clause justifies the proof's *generality* rather than advancing the proof. It reads as residue from the decoupling revision (Issue 1's sibling). The domain is already fixed by the contract's preconditions (p ∈ T, d ≥ 1); restating it as a defense is noise.
**Required**: Drop the justifying clause; open with the substantive step ("c₁ = inc(p, d) ∈ T … each increment strictly advances its argument by TA5(a)").

## OUT_OF_SCOPE

### Topic 1: Alignment of allocator domains with the baptismal registry
**Why out of scope**: The open question "Under what activation discipline does `allocated(s) ⊆ s.B` hold" is genuinely new territory — it requires a mapping between foundation allocator transitions and baptismal operations that this ASN does not (and need not) establish. Correctly deferred.

### Topic 2: Cross-replica baptism ordering
**Why out of scope**: B8's co-reachability restriction (single transition path) is the correct and necessary scoping for a single-history registry; global uniqueness across divergent replicas depends on the inter-server protocol, properly listed as a future concern.

VERDICT: REVISE
