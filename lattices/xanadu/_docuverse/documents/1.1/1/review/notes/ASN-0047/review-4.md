# Review of ASN-0047

## REVISE

### Issue 1: P6 derivation invokes J0 for something J0 does not establish

**ASN-0047, Temporal decomposition / P6**: "The document must be in E'\_doc for its arrangement to receive a (J0); once in E\_doc, P1 preserves it."

**Problem**: J0 establishes that *some* document `d ∈ E'_doc` contains the freshly allocated address `a` in its arrangement. It does not establish that `origin(a)` specifically is in `E_doc`. The existentially quantified `d` in J0 need not be `origin(a)` — content allocated under `origin(a)`'s prefix could appear in a *different* document's arrangement (this is precisely what transclusion does). The derivation conflates "the document whose arrangement receives `a`" with "the document whose prefix was used to allocate `a`."

**Required**: Replace the J0 argument with the correct one: allocation under `origin(a)`'s prefix (S7a) requires `origin(a)` to exist as a document entity — the allocation mechanism (`inc(·, k)` within an ownership domain, T10/TA5, ASN-0034) operates on existing tumblers. State this as an explicit precondition of K.α (that the creating document is in `E_doc`) or as a bridging argument from the allocation mechanism to the entity set. The derivation chain should be: K.α allocates `a` under `origin(a)`'s prefix → allocation requires `origin(a) ∈ E_doc` (by allocation mechanism) → P1 preserves membership → P0 preserves `a ∈ dom(C)`.

### Issue 2: Worked example does not exercise destructive transitions

**ASN-0047, Worked example**: "The two scenarios exercise J0, J1, J4, P4, P5, P6, and P7"

**Problem**: Both scenarios (fork, insertion) are purely constructive — K.δ, K.α, K.μ⁺, K.ρ. Neither K.μ⁻ (contraction) nor K.μ~ (reordering) is exercised, so J2 (contraction isolation) and J3 (reordering isolation) receive no concrete verification. The ASN calls J2 "the deepest consequence of the design" — that deletion is purely presentational and R preserves stale entries. This central claim deserves a concrete demonstration: a deletion step showing `Contains(Σ)` shrinking while R does not, producing the divergence between current containment and historical provenance that the prose describes at length.

**Required**: Add a third step to the worked example: delete one character from d₂ (K.μ⁻). Show: (1) the mapping is removed from M(d₂), (2) C, E, R are all unchanged (J2), (3) `Contains(Σ₄) ⊂ Contains(Σ₃)` while `R₄ = R₃` — the stale entry persists. This grounds J2 and the provenance-divergence property concretely.

## OUT_OF_SCOPE

### Topic 1: Bootstrap and initial entity creation
K.δ describes allocation "under the parent's prefix," but the first entity (first node) has no parent. The transition from Σ₀ = (∅, ∅, λd.⊥, ∅) to a state with entities requires a bootstrap mechanism not covered here.
**Why out of scope**: This is system initialization / operational specification, not state transition taxonomy.

### Topic 2: Link-specific transition constraints
Links are included in E\_doc but their endset management, bidirectional index maintenance, and subspace layout are deferred.
**Why out of scope**: The ASN explicitly defers the structural distinction between documents and links. Link semantics are a future ASN.

VERDICT: REVISE
