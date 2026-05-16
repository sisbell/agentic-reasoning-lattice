# Review of ASN-0047

## REVISE

### Issue 1: Notation inconsistency in ExtendedReachableStateInvariants theorem statement

**ASN-0047, Extended reachable-state invariants**: "satisfies: S0 ∧ S1 ∧ S2 ∧ S3★ ∧ S3★-aux ∧ S4 ∧ S7a ∧ S7b ∧ S7c ∧ S7d ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧ S9 ∧ D-CTG ∧ D-MIN ∧ D-SEQ★ ∧ P4★ ∧ ..."

**Problem**: The theorem mixes unstarred D-CTG / D-MIN with the starred D-SEQ★. Throughout this ASN, "D-CTG" and "D-MIN" are aliased to the per-subspace forms D-CTG★ and D-MIN★, but the foundation ASN-0036's D-CTG and D-MIN explicitly exempt the link subspace. Since reviewers must verify the conjunction against both foundations and this ASN's amendments, the surface ambiguity matters: the theorem's literal conjuncts would be unsatisfiable in the extended state (ASN-0036's D-CTG/D-MIN exempt s_L; reachable states under the extended transition system arrange link-subspace positions and must satisfy contiguity there).

**Required**: Replace D-CTG and D-MIN with D-CTG★ and D-MIN★ in the theorem statement and in any other formal conjunction. Reserve the unstarred names exclusively for the imported ASN-0036 statements (or drop them from this ASN entirely).

### Issue 2: K.μ~ redundancy argument's conclusion is weaker than its claim

**ASN-0047, Generalized referential integrity / Link-subspace fixity under K.μ~**: "the redundancy argument therefore recovers the link-subspace identity clause from the weaker subspace-preservation clause via S3★; the definition-site precondition is consistent with — and structurally compelled by — the rest of the model."

**Problem**: The argument concludes `M'(d)|_{dom_L} = M(d)|_{dom_L}` (function-level equality on dom_L). It does *not* derive `π(v) = v` for every `v ∈ dom_L`. Under K.μ⁺_L's stated preconditions, nothing prevents two K.μ⁺_L invocations from placing the same ℓ at distinct link-subspace V-positions (the precondition forbids only V-position collision, not range duplication). With duplicate values admissible, a non-identity π on dom_L that swaps two positions sharing a value satisfies both the K.μ~ defining equation and the chained function equality. The redundancy argument therefore compels the *effect* on dom_L (the function M'(d)|_dom_L is identity-equivalent) but does not compel the *bijection* π = id on dom_L.

**Required**: Either (a) state and prove a uniqueness invariant on link-subspace mappings within a document (`(A v₁, v₂ ∈ dom_L(M(d)) : v₁ ≠ v₂ : M(d)(v₁) ≠ M(d)(v₂))`) and derive position fixity from it; or (b) rephrase the redundancy argument's conclusion to say that the K.μ~ identity clause picks a canonical representative among value-preserving permutations on dom_L, all of which produce the same M'(d). Without one of these, the claim "structurally compelled" overreaches.

### Issue 3: K.δ k=1 case for non-document entities is unspecified

**ASN-0047, K.δ (Entity creation), case (ii)**: "*Sibling-at-deeper-tumbler-depth (k = 1).* TA5(d) with `k = 1` appends `.1` and introduces no new zero separator..., so `zeros(e) = zeros(t)`."

**Problem**: The ASN provides a detailed harmlessness verification only for the case t = a document (`zeros(t) = 2`), treating k = 1 as creating a document version. But K.δ's precondition for ¬IsNode admits k ∈ {0, 1, 2} when t is an account (`zeros(t) = 1`) or a sibling at any non-node level. K.δ with t an account and k = 1 produces `e = inc([N,0,U], 1) = [N,0,U,1]` with zeros(e) = 1 — an account-shaped sibling at deeper tumbler depth. The ASN does not say whether such "account versions" are intended, what their semantics are, or whether the harmlessness verification covers them. The structural admissibility under T10a is the same, but Nelson's design and Gregory's implementation do not address account or node versioning.

**Required**: Either (a) explicitly admit account/node "versions" with a sentence stating that the harmlessness verification extends symmetrically (and confirming all invariants hold for k = 1 from accounts and nodes), or (b) restrict K.δ's k = 1 case to t with `IsDocument(t)` via precondition, or (c) add this to the open questions as deferred semantics.

### Issue 4: ExtendedReachableStateInvariants proof omits explicit P8 check for K.δ

**ASN-0047, Extended reachable-state invariants proof, Class (a) for K.δ**: "For K.δ, K.ρ: hold both M and L in frame; C, L unchanged; S3★, S3★-aux preserved (M unchanged); link invariants preserved since neither L nor dom(C) is modified."

**Problem**: P8 (entity hierarchy) is the load-bearing invariant K.δ must preserve, and K.δ is the *only* transition that can violate it. The proof's K.δ paragraph addresses every invariant except P8 explicitly. The reader is expected to recall P8's separate derivation paragraph (where preservation is sketched), but the inductive case analysis at the proof site should be self-contained.

**Required**: Add a sentence in K.δ's case: "P8: for K.δ with ¬IsNode(e), the precondition parent(e) ∈ E supplies the new entity's parent in E; subsequent transitions preserve parent(e) ∈ E by P1. For IsNode(e), the P8 universal excludes the new entity vacuously."

### Issue 5: K.μ⁻ admissibility for the link subspace is not exercised in any worked example

**ASN-0047, Consequence for link withdrawal (after D-CTG★/D-MIN★ amendment)**: "a user cannot withdraw a single link at a non-maximum link-subspace position while leaving subsequent links in place... withdrawing one interior link requires withdrawing every link allocated after it as well."

**Problem**: This consequence is structurally significant — it diverges sharply from Nelson's tombstoning design — but no worked example demonstrates either the admissible cases (suffix withdrawal of multiple links, full link-subspace clearance) or the inadmissible ones (single-interior withdrawal). The second worked example exercises K.λ, K.μ⁺_L, and K.μ~ on link-subspace mappings but never K.μ⁻ on s_L. Per the standards ("Boundary cases mandatory") and given that this is the most consequential change to the foundation ASN-0036's invariants, an example is needed.

**Required**: Add a fourth step to the second worked example demonstrating K.μ⁻ on the link subspace — e.g., allocating a second link via K.λ + K.μ⁺_L, then showing (a) suffix removal of the most recent link is admissible, and (b) attempted removal of the older link alone is inadmissible (citing the case-(b) interior-removal forbidance). Verify D-CTG★, D-MIN★, S3★, CL-OWN at each step.

### Issue 6: L3 amendment's downstream consequences are unstated

**ASN-0047, Link store and extended system state, L3**: "ASN-0043's non-empty type-endset clause (`Σ.L(a).e₃ ≠ ∅`) is dropped — the abstract model admits empty Θ as a well-formed link value..."

**Problem**: ASN-0043's L3 (with `Θ ≠ ∅`) is referenced by L8 (TypeByAddress, type matching) and L10 (TypeHierarchyByContainment). Under this ASN's weakened L3, the equivalence relation `same_type` becomes degenerate on links with `Θ = ∅` — `coverage(∅) = ∅`, so all untyped links would be same_type-equivalent (all having empty coverage). The ASN does not address whether this collapse is intended, nor whether downstream operations should treat untyped links specially. Within this ASN's transition contracts, no downstream consequence arises (K.λ admits empty Θ; K.μ⁺_L treats ℓ as opaque). But the silence on the downstream effects leaves the model ambiguous: is empty-Θ semantically "an untyped link" (the prose claim) or "a link sharing the trivial type" (the L8 consequence)?

**Required**: Add a sentence either (a) restricting same_type's domain to links with Θ ≠ ∅ (and noting empty-Θ links are outside the equivalence), or (b) explicitly accepting that all empty-Θ links share a single equivalence class under same_type and noting the consequence.

### Issue 7: Allocator hierarchy claim's cross-document disjointness leans on T10 without explicit instantiation

**ASN-0047, Allocator hierarchy under documents**: "By T10 (PartitionIndependence), link addresses in different documents cannot collide either."

**Problem**: T10's hypothesis is `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` for two prefixes. The sub-allocator anchors `b_L(d₁) = [d₁.0.s_L]` and `b_L(d₂) = [d₂.0.s_L]` are extensions of d₁ and d₂ respectively. T10 applied to d₁ and d₂ (the document tumblers) requires d₁ ⋠ d₂ ∧ d₂ ⋠ d₁, which follows from T10a.6 (DomainDisjointness) plus the fact that K.δ allocates documents under distinct accounts via independent inc-conformance. But the ASN does not chain T10a.6 + T10 explicitly — it gestures at T10 as if its hypothesis were obvious. For two documents under the *same account* — d₁ = [N,0,U,0,1] and d₂ = [N,0,U,0,2] — neither is a prefix of the other (by T10a.6 over the account's allocator), so T10 applies. For two documents under different accounts, similarly. The chain is short but should be made explicit, especially because the sub-allocator anchors *under* d₁ and d₂ are what matter, and extensions of incomparable prefixes are also incomparable only after one more T10/T5 step.

**Required**: Replace "By T10 (PartitionIndependence)..." with a one-sentence chain: "T10a.6 gives d₁ ⋠ d₂ ∧ d₂ ⋠ d₁ for distinct documents; T10 instantiated at p₁ = b_L(d₁), p₂ = b_L(d₂) — which inherit the non-nesting from their respective document prefixes — gives disjointness of any addresses extending the two anchors."

## OUT_OF_SCOPE

### Topic 1: Link withdrawal mechanism

The ASN's D-CTG★ forbids single-interior link removal via K.μ⁻; Nelson's tombstoning design (LM 4/9) is the intended mechanism but is not provided here. Acknowledged in the open questions as deferred.

### Topic 2: Concurrent allocation, atomicity, and ordering

The "what must the system guarantee about concurrent operations" question is in the open questions. The transition model is sequential.

### Topic 3: Operation-level specifications (INSERT, DELETE, COPY, REARRANGE, MAKELINK)

Explicitly out of scope per the Scope section. The ASN provides elementary transitions and composites (J4) from which operations would be specified in subsequent ASNs.

### Topic 4: Forking with link inheritance

J4 transcludes only content. Link inheritance under forking is not supported; the ASN defers a mechanism to a future ASN.

VERDICT: REVISE
