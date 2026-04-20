# Review of ASN-0079

## REVISE

### Issue 1: F0 — Derivation through wrong foundation
**ASN-0079, "From Visible Content to Content Identity"**: "This transparency is not a special rule for transclusion. It is a direct consequence of the two-stream separation (S9, ASN-0036)"
**Problem**: S9 states that arrangement changes cannot alter the content store. F0 claims that resolution produces the same I-addresses regardless of which document's arrangement is used. These are different properties. S9 is about C being invariant under M changes; F0 is about the `addresses()` function extracting the same I-addresses from any M(d) containing them. The derivation should go through the resolution definition (ASN-0058), not S9.
**Required**: Derive F0 explicitly: (1) v₁ ∈ ⟦σ₁⟧ by "spanning v₁"; (2) well-formedness places v₁ ∈ dom(f) where f = M(d₁)|⟦σ₁⟧; (3) by C1a (ASN-0058) v₁ belongs to some block βⱼ = (vⱼ, aⱼ, nⱼ); (4) by B3, M(d₁)(v₁) = aⱼ + k; (5) therefore a = aⱼ + k ∈ addresses(d₁, σ₁). S9 is correct conceptual motivation but not the proof mechanism.

### Issue 2: F8 — Statement ambiguous about home constraint; proof omits three conjuncts
**ASN-0079, "Transclusion Transparency"**: "for any query Q constraining slot i with a set P ∋ a (and all other slots unconstrained): ℓ ∈ FindLinks(Q)"
**Problem**: "All other slots unconstrained" is ambiguous about whether H is among the "other slots." The query specification Q = (H, S₁, S₂, S₃) has four components; "slot i" names Sᵢ, but the home constraint H is structurally distinct from the three endset constraints. If H ≠ ⊤ and home(ℓ) ∉ H, the claim fails. The proof then addresses only sat(eᵢ, P), leaving the home constraint, sat(eⱼ, ⊤) for j ≠ i, and sat(eₖ, ⊤) unmentioned — three of four conjuncts in F1 are absent.
**Required**: (a) State explicitly: "with H = ⊤ and Sⱼ = ⊤ for j ≠ i". (b) The proof should note: "With H = ⊤, the home constraint is trivially satisfied; with Sⱼ = ⊤ for j ≠ i, sat(eⱼ, ⊤) = true by definition. The remaining condition is sat(eᵢ, P)."

### Issue 3: F18 — Imprecise citation for dom(L) membership
**ASN-0079, "FINDLINKS as a Derived Operation"**: "T8 (AllocationPermanence, ASN-0034) preserves a ∈ dom(Σ'.L)"
**Problem**: T8 is about tumbler allocation permanence in the address space T — "If tumbler a ∈ T has been allocated at any point in the system's history, then for all subsequent states, a remains in the set of allocated addresses." This does not directly establish membership in dom(L). The correct property is L12 (LinkImmutability), which the proof already cites for value preservation and which directly establishes both: `a ∈ dom(Σ.L) ⟹ a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`.
**Required**: Replace the T8 citation with L12, which provides both membership preservation and value preservation in a single property. The proof already cites L12 for the value half; it should cite L12 for both.

### Issue 4: F19 — Ambiguous complexity phrasing
**ASN-0079, "Scale"**: "Any conforming implementation must maintain index structures enabling sublinear candidate location — at minimum O(log |dom(Σ.L)|) to reach the matching region."
**Problem**: "At minimum O(log n)" is ambiguous. It could mean (a) Ω(log n) is a lower bound on any implementation (no tree-based index can do better), or (b) the specification requires implementations to achieve at most O(log n). The formal requirement F19 says "sublinear," which is weaker than O(log n). The phrase conflates a lower bound on implementation cost with an upper bound on required complexity.
**Required**: Separate the two claims. F19 requires sublinear candidate location — o(|dom(L)|). The parenthetical can observe that tree-based indexing achieves Θ(log |dom(L)|) traversal cost, and that Ω(log |dom(L)|) is a comparison-based lower bound for key lookup. These are different statements and should not be fused with "at minimum."

## OUT_OF_SCOPE

### Topic 1: Concurrency and isolation for FINDLINKS
**Why out of scope**: The ASN defines FINDLINKS at a single fixed state Σ. Isolation guarantees when link creation and link search execute concurrently require a concurrency model not established by any foundation ASN. Correctly deferred to open questions.

### Topic 2: Prefix-based search constraints for type hierarchy queries
**Why out of scope**: The SearchConstraint requires a finite set P ⊂ T, while type hierarchy queries via L10 (ASN-0043) use prefix spans covering infinite subtree sets. Extending the constraint language to support prefix-based matching is new machinery beyond this ASN's scope. The ASN correctly notes L10 as context for why P may contain non-dom(C) addresses, without claiming the finite-P framework fully supports hierarchy queries.

### Topic 3: Pagination stability under link store growth
**Why out of scope**: F6 defines deterministic pagination for fixed Σ. What happens when dom(L) grows between page requests (new links created that satisfy Q) requires a snapshot or versioning model. Correctly deferred to open questions.

VERDICT: REVISE
