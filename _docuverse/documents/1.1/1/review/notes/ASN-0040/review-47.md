# Review of ASN-0040

## REVISE

### Issue 1: B7 and B8 re-derive foundation results for what are literally allocator domains
**ASN-0040, §Namespace disjointness / §Global uniqueness**: B7 proves `S(p, d) ∩ S(p', d') = ∅` from T3, T10, S1 primitives; B8 states "B8 restates ASN-0034's GlobalUniqueness at the namespace level."
**Problem**: Under B6, every stream `S(p, d)` is exactly the domain of the child allocator spawned by `inc(p, d)` with `d ∈ {1,2}` (T10a's child-spawn `inc(t, k')`, `k' ∈ {1,2}`, then siblings via `inc(·, 0)`). Distinct B6-valid pairs are therefore distinct allocators, and "stream disjointness" is precisely T10a.6 (DomainDisjointness) / T10a.5 (CrossAllocatorIncomparability). The foundation already proves this; the ASN re-derives it without connecting `S(p, d)` to the allocator domain it is.
**Required**: Either explicitly identify `S(p, d)` as the child-allocator domain and discharge B7/B8 by citing T10a.5/T10a.6/GlobalUniqueness, or state precisely what B7/B8 add beyond the foundation (the registry-level contiguity/no-skip refinement is the only genuinely new content, and it should be isolated as such).

### Issue 2: B8 Case 1 asserts comparability of the two acts without grounding
**ASN-0040, §Global uniqueness, B8 proof Case 1**: "Without loss of generality, β₁ precedes β₂ in that sequence... Since β₁ precedes β₂, s₂ is reachable from s₁'."
**Problem**: The state space is described as a general Kripke space with reflexive-transitive closure reachability. Two distinct baptismal acts need not be linearly ordered (they may lie on incomparable branches), so the WLOG step is unjustified as written. The intended reading — that within any single reachable state the producing acts share a totally-ordered history — is never stated.
**Required**: Restrict the claim to acts along the history of a single reachable state (or otherwise justify that the two acts are comparable), then the `s₁' →* s₂` step is licensed.

### Issue 3: Dependency-justification ("why X is needed") meta-prose
**ASN-0040, §The contiguous prefix property** ("Two dependencies bear emphasis. B7... ensures... B0a... ensures... without B0a, a non-baptismal operation could insert..."); **§The high water mark** ("Without B1, the count would not determine the maximum... Without S0, even a contiguous prefix need not... Both properties are required..."); **§B₀ conf.** ("These three structural conditions are individually necessary. Finiteness is required because... Without the contiguity requirement... Without the T4 requirement...").
**Problem**: These paragraphs explain *why* a cited dependency is needed rather than advancing the claim. This is the flagged "use-site inventory / why-the-axiom-is-needed" pattern; the Depends/Preservation lines in the Formal Contracts already record the dependencies.
**Required**: Delete the why-needed prose. The dependency citations in the contracts carry the load; the necessity arguments that are genuine content (B₀ conformance necessity) can be reduced to the contract's Base/Preservation lines.

### Issue 4: Essay content in structural slots
**ASN-0040, §The high water mark** (after B2): "Two systems beginning from the same B₀ and executing the same sequence of baptisms... produce identical address spaces. The addresses are not identifiers assigned by fiat; they are the inevitable consequence of the baptism history."; **§The baptismal registry**, B0 paragraph: "This is the state-level reading of T8... T8 says the allocator never reclaims an address; B0 says the registry never shrinks..."
**Problem**: The determinism remark is a derived consequence stated without derivation (essay content); the B0/T8 comparison is interpretive meta-prose, not part of the corollary's statement.
**Required**: If determinism is a claim, state it as a property with a proof; otherwise delete. Reduce the B0 paragraph to the corollary and its one-line derivation from B0a.

### Issue 5: Downstream-deferral paragraph contributing no local reasoning
**ASN-0040, §State space and transitions** ("Relationship to ASN-0034's allocated set"): "The inclusion `allocated(s) ⊆ s.B` holds only conditionally on the activation-discipline ASN... both discharges belong to that ASN."
**Problem**: The paragraph states a relation this ASN does not establish and defers it wholesale to a future ASN. It is the flagged "multiple paragraphs defer to the same downstream location" pattern and advances no reasoning here.
**Required**: Reduce to a one-line forward note, or move to Open Questions where the same deferral already lives.

### Issue 6: B1 proof's exhaustiveness-claim framing
**ASN-0040, §The contiguous prefix property, B1 proof**: "The case analysis is exhaustive over arbitrary (p, d) ≠ (p₀, d₀). We split first on whether... This yields three sub-cases... Which configurations fall under (B) versus (C) is exactly B6's necessity result..."
**Problem**: A meta-paragraph announcing the structure and exhaustiveness of the case split precedes the split itself; the routing-rationale ("(B) versus (C) is exactly B6's necessity") is bookkeeping about another claim rather than the argument. This is the flagged exhaustiveness-claim pattern.
**Required**: Open each sub-case directly with its hypothesis (A/B/C). The split is self-evidently exhaustive once the cases are stated; the framing paragraph can be removed.

## OUT_OF_SCOPE

### Topic 1: B3 (Ghost Validity) formal forward-requirement on `Occupied`
**Why out of scope**: Content storage and retrieval are explicitly out of scope. The motivating ghost-element concept (a position in `s.B` with nothing stored) is in-scope and correctly grounded in Nelson, but the formal four-way `Occupied`-classification and the constraint `Occupied(t, s) ⟹ t ∈ s.B` are claims about a content predicate this ASN does not define. They belong to the future content-storage ASN; here they are forward-reference accretion. Keep the one-sentence ghost-element observation; move the parametric classification table and the forward requirement out.

### Topic 2: Parent-prerequisite chain (B6 "no parent-baptized prerequisite is imposed")
**Why out of scope**: Whether a parent must be baptized before its children is correctly deferred to the ownership model (Open Question 1). No revision needed — flagged only to confirm the deferral is appropriate, not an error.

VERDICT: REVISE
