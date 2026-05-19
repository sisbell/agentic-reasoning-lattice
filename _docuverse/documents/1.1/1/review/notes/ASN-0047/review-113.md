# Review of ASN-0047

## REVISE

### Issue 1: Partial-suffix admissibility "iff" claim is incorrect

**ASN-0047, "Decomposition of K.μ~" section**: "This expansion is admissible iff π preserves M(d)-values below the cut pointwise: `(A v ∈ V_{s_C}(d) : v < [s_C, 1, ..., 1, k₀] under the V-ordering on s_C : M(d)(π(v)) = M(d)(v))`."

**Problem**: The stated condition is necessary but not sufficient. The quantifier is over v below the cut (v ∈ X) with the M(d)-comparison at π(v) (forward image). This captures the X→X bijection obligation but misses the Y→X obligation. For v ∈ Y with π(v) ∈ X, the bijection equation M'(d)(π(v)) = M(d)(v) forces M(d)(π(v)) = M(d)(v) (since π(v) is a survivor with M_int(d)(π(v)) = M(d)(π(v))) — but the ASN's quantifier never reaches v ∈ Y.

**Counterexample**: Take V_{s_C}(d) = {x1, x2, y1, y2} = {[1,1], [1,2], [1,3], [1,4]} at k₀ = 3 (X = {x1, x2}, Y = {y1, y2}), with M(d) values {x1→a, x2→b, y1→a, y2→b}. Consider the 4-cycle π: x1→y1, y1→x2, x2→y2, y2→x1. ASN's stated constraint at x1: M(d)(y1)=a=M(d)(x1) ✓; at x2: M(d)(y2)=b=M(d)(x2) ✓. ASN admits. But realizing K.μ⁻ at k₀=3 then K.μ⁺: M_int = {x1↦a, x2↦b}; K.μ⁺ adds (y1, M(d)(x1))=a and (y2, M(d)(x2))=b. The bijection equation at y1 (π(y1)=x2): M'(d)(x2) = M(d)(y1) → b = a. Contradiction. Partial-suffix fails despite the stated condition holding. (Full clearance at k₀=1 still realizes π correctly.)

**Required**: Restate as "for all v ∈ V_{s_C}(d) with π(v) below the cut, M(d)(π(v)) = M(d)(v)" — equivalently "for all u ∈ X, M(d)(u) = M(d)(π⁻¹(u))" — which captures both X→X and Y→X obligations. Alternatively, weaken "iff" to "necessary" and note that sufficiency requires the additional Y→X clause.

### Issue 2: Cross-document distinctness for K.δ documents has argument gap

**ASN-0047, "K.δ case (ii) discharge and parent-allocator activation" section, sub-case A discharge**: "*Cross-document distinctness for K.δ documents* (parent(d₁) ≠ parent(d₂)): the Cross-document disjointness chain lemma applies at the account level — instantiated at `e₁ = A₁, e₂ = A₂` with `s = 1`... together with T10 (PartitionIndependence) gives `d₁ ≠ d₂` for any document minted under each account."

**Problem**: The lemma+T10 chain only delivers distinctness between addresses that *extend* the anchors [A_1.0.1] and [A_2.0.1] under the prefix relation ≼. The document sub-allocator A_doc(A_i) emits siblings [A_i.0.1], [A_i.0.2], [A_i.0.3], ... at uniform length #A_i+2; for k ≥ 2, [A_i.0.k] is **not** an extension of [A_i.0.1] (same length, prefix-incomparable at the terminal position). Hence T10 with p_i = [A_i.0.1] does not cover documents at sibling positions [A_1.0.k] vs [A_2.0.k'] for k, k' ≥ 2. The conclusion holds via a different argument, but the cited chain is incomplete.

**Required**: Apply the lemma's case-analysis at the entity level — instantiate at e_1 = A_1, e_2 = A_2 themselves to derive A_1 ⋠ A_2 ∧ A_2 ⋠ A_1 (Case B). Then apply T10 with p_1 = A_1, p_2 = A_2: every [A_1.0.k] extends A_1 (since A_1 ≼ [A_1.0.k]) and every [A_2.0.k'] extends A_2, so T10 directly yields distinctness across all k, k' ≥ 1.

### Issue 3: K.α amendment framing inconsistency

**ASN-0047, "Amendments to existing transitions" section**: "**K.α (no separate amendment in extended state).** ... References elsewhere in this ASN to 'the K.α amendment' (in the verification matrix and discharge prose below) name the same content-subspace restriction — now interpreted as the inherited foundation precondition, not a local addition."

**Problem**: The opening declares "no separate amendment" but the verification matrix and elsewhere repeatedly cite "K.α amendment" as if it were a local construct (e.g., "S7b: K.α amendment + content sub-allocator chain ⟹ zeros(a)=3"; "L14: K.α amendment ⟹ subspace_I(a)=s_C ≠ s_L"; "L0 (C-clause): K.α amendment: subspace_I(a)=s_C"). Readers must reconcile "no amendment exists" with "the amendment" appearing 6+ times in citations. Either the term names something or it doesn't.

**Required**: Either remove all references to "K.α amendment" and cite "ASN-0093's K.α precondition E(a)₁=s_C" directly at each occurrence, or define "K.α amendment" once as a documented shorthand for that inherited precondition and apply uniformly.

## OUT_OF_SCOPE

The ASN's "Open Questions" section already itemizes future-ASN concerns (fork-source invariants, transitive transclusion provenance, link discoverability under contraction, version-arrangement lineage relationships, link permanence for content participating in endsets, additional link-subspace invariants, address-space exhaustion guarantees, concurrent operations, node registry protocol abstraction, link withdrawal mechanism, account-level depth-1 extension). None of these should be flagged as missing from this ASN — they belong in future ASNs.

VERDICT: REVISE
