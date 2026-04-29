# Review of ASN-0043

## REVISE

### Issue 1: Link value immutability is unaddressed
**ASN-0043, Link Distinctness and Permanence**: L12 states `(A Σ, Σ' : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L))`
**Problem**: For content, S0 (ASN-0036) establishes both persistence and immutability: `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. L12 establishes only the first half — the address endures. Whether `Σ'.L(a) = Σ.L(a)` holds across state transitions is never stated.

This is not an operational question. The ASN defines what a link IS — an addressed triple of endsets. Whether that triple is immutable after creation is fundamental to the entity's nature. If link values are immutable, L12 should say so, completing the parallel to S0. If link values are mutable (endsets can be updated after creation), the ASN introduces a deep asymmetry with content that needs explicit justification. Mutability also affects the meaning of L11: if endsets can change, then "identity by address" means two temporal snapshots of the same link can have different endsets while sharing the same identity — a very different semantic regime from content, where identity and value are permanently fused.

**Required**: Either strengthen L12 to include `Σ'.L(a) = Σ.L(a)` (immutability, parallel to S0), or introduce a weaker property (address permanence without value immutability) with explicit discussion of the asymmetry.

### Issue 2: L4 asserts what the Open Questions leave unsettled
**ASN-0043, Endset Properties**: "There is no constraint confining spans to a single document, to content addresses only, or to addresses at which content currently exists"
**Problem**: L4 positively asserts that no existence constraint applies to endset spans. The Open Questions then ask: "Must the from and to endsets of a well-formed link reference addresses in `dom(Σ.C)`, or is a link well-formed even when its content endsets reference addresses at which no content exists?" If L4 already answers this (no constraint), the question is moot and should be removed. If the question is genuinely open, L4 overstates.

The same tension appears between L4(c) (cross-subspace endsets permitted) and the Open Question about spans extending across subspace boundaries; and between L9 (type endsets may reference ghost addresses) and the Open Question about whether every link must have a non-empty type endset. In each case, the property section asserts a definitive answer while the Open Questions section treats it as unresolved.

Similarly, the Endset definition permits empty endsets (`∅ is a valid endset`) while the Open Questions ask whether a link without type classification is well-formed. The definition has already settled the matter by allowing it.

**Required**: Audit every Open Question against the stated properties. For each conflict, either weaken the property to leave the question open, or remove the question. A property and a question about the same matter cannot coexist.

### Issue 3: Coverage derivation from L5 is a non-sequitur
**ASN-0043, Coverage definition**: "By L5, coverage is the semantically meaningful content of an endset — the identity of which addresses are referenced, not how the reference is decomposed into spans."
**Problem**: L5 says an endset is an unordered set of spans — ordering carries no semantic weight. This means `{(s₁, ℓ₁), (s₂, ℓ₂)} = {(s₂, ℓ₂), (s₁, ℓ₁)}`. It does NOT mean that `{(1, [3])}` and `{(1, [1]), (2, [2])}` are equivalent, even when both cover the same addresses. These are different sets containing different spans. L5 collapses permutations of the same collection; it does not collapse distinct collections with the same union.

The "By L5" implication is incorrect. This creates a three-way contradiction: (a) L5 implies span-level identity — different span decompositions yield different endsets, (b) the Coverage sentence claims coverage-level identity — decomposition is irrelevant, and (c) the Open Questions ask "are two endsets with different span decompositions but identical coverage equivalent?" — a question already answered by L5 (no) and simultaneously answered by Coverage (yes).

**Required**: Commit to one identity criterion. If span-level (L5 as stated): remove the "By L5" sentence and acknowledge that `coverage` is a lossy projection — it maps distinct endsets to the same address set. Two endsets with identical coverage but different span decompositions are distinct objects. If coverage-level: redefine endset equality as coverage equality (formally: `e₁ ≡ e₂ ⟺ coverage(e₁) = coverage(e₂)`) and note that L5 follows as a consequence, since reordering spans preserves coverage. Then remove the corresponding Open Question.

### Issue 4: L10 has no formal statement
**ASN-0043, The Type Endset**: "When type addresses are chosen with hierarchical structure, the tumbler containment relation (T5, T6, ASN-0034) provides subtype-supertype relationships without any additional mechanism."
**Problem**: Every other numbered property (L0–L9, L11–L14) has a formal statement in quantified or equational form. L10 is prose and a worked example only. The claim is substantive — it connects tumbler prefix ordering to type semantics — but it is never formalized. What precisely does "provides subtype-supertype relationships" mean in terms of span queries and address matching?
**Required**: Provide a formal statement. For example: for type addresses `p` and `c` where `p ≼ c`, define `subtypes(p) = {c ∈ T : p ≼ c}`. Then by T5, `subtypes(p)` is a contiguous interval under T1, so a single span `(p, ℓ)` with appropriately chosen width covers all subtypes. The formalization should also state whether subtype matching is the responsibility of the link store or of query operations (which may push it to OUT_OF_SCOPE).

### Issue 5: L14 exhaustiveness uses undefined "all stored addresses"
**ASN-0043, The Dual-Primitive Architecture**: `{all stored addresses} = dom(Σ.C) ∪ dom(Σ.L)`
**Problem**: The full state is `Σ = (Σ.C, Σ.M, Σ.L)`. The domain `dom(Σ.M(d))` contains V-positions that are in neither `dom(Σ.C)` nor `dom(Σ.L)`. The intent is that V-positions are arrangement keys, not stored entities, but this distinction is informal. "Stored address" does real work in the claim — it is what excludes V-positions and structural tumblers like document prefixes — yet it is never defined.
**Required**: Define "stored address" precisely, or reformulate L14 without it. One option: "The set of addresses at which entity values reside is `dom(Σ.C) ∪ dom(Σ.L)`. No state component maps an address outside this union to an entity value. Arrangements `Σ.M(d)` are mappings *between* addresses, not entity stores."

### Issue 6: Non-transclusion claim is asserted without derivation
**ASN-0043, The Dual-Primitive Architecture**: "Link identity is unique: each link has exactly one address, and there is no mechanism to make two documents 'share' the same link. [...] It cannot be transcluded into another owner's authority."
**Problem**: This is a strong design claim stated without derivation. The proof is two steps: S3 (ASN-0036) requires `Σ.M(d)(v) ∈ dom(Σ.C)` for every V-mapping; L0 establishes `dom(Σ.L) ∩ dom(Σ.C) = ∅`. Together these entail that no arrangement can map a V-position to a link address, so the transclusion mechanism (multiple arrangements referencing the same I-address) cannot apply to links. The derivation is short but the conclusion is architecturally significant — it should be shown, not asserted.
**Required**: Add the two-step derivation (S3 + L0) where the non-transclusion claim is made.

## OUT_OF_SCOPE

### Topic 1: Endset span normalization
**Why out of scope**: Whether distinct span decompositions with identical coverage should be treated as equivalent is an algebraic property of endsets. The ASN correctly identifies this as an open question (once Issue 3 is resolved to establish the baseline identity criterion). Normalization rules belong in a future ASN that addresses endset algebra.

### Topic 2: Compound link well-formedness constraints
**Why out of scope**: The ASN establishes that link-to-link references are structurally possible (L13) but correctly defers constraints on compound link structures — acyclicity, depth bounds, referential integrity of link-to-link chains. These are structural properties of link graphs, not of individual links.

### Topic 3: Link allocation ordering relative to content
**Why out of scope**: The ASN establishes disjoint subspaces (L0) but correctly defers questions about interleaving of link and content allocation within a document. This is an operational concern within the explicitly excluded scope.

VERDICT: REVISE
