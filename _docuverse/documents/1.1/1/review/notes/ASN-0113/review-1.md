# Review of ASN-0113

## REVISE

### Issue 1: W12 existential is asserted "immediate," never constructed
**ASN-0113, "What the pair reveals"**: "The construction is immediate: the two subspaces are independently populated (W14, below), so a document with `c` characters admits any link count, and conversely."
**Problem**: W12's formal content is an *existence* claim — for any `c, k₁, k₂` there exist documents `d₁, d₂` with the stated profiles. This is a reachability/constructibility assertion (the analogue of ASN-0036's S5 UnrestrictedSharing), and it is discharged only by the words "immediate." Two further defects compound this:
  - The cited support "independently populated (W14, below)" names the **wrong claim**: W14 is Comparability; independence is W15.
  - Even W15 (Independence) establishes only that the projection *functions* don't cross-depend — it does **not** establish that documents realizing arbitrary `(n_{s_C}, n_{s_L}) ∈ ℕ × ℕ` are reachable. Functional independence is not surjectivity onto the profile lattice.
The quantifiers in the formal statement also leave `c, k₁, k₂` untyped (no `∈ ℕ`).
**Required**: Either exhibit a construction of documents with arbitrary independent text/link extents (a reachability argument over K.δ/K.μ⁺/K.μ⁺_L from ASN-0047), or invoke an existing foundation existence lemma. Fix the cross-reference and type the quantified variables.

### Issue 2: W5 biconditional has only one direction proved
**ASN-0113, "Exactness is contingent on contiguity"**: "W4 holds for each subspace precisely when that subspace's active positions are contiguous; absent contiguity a single per-subspace span can only *bound*, not exactly cover."
**Problem**: "precisely when" is a biconditional. The contiguous ⟹ exact direction is established (W4, via D-SEQ★). The converse — non-contiguous ⟹ no single span is exact over the V-slice — is only sketched ("a single span... would *overshoot*, including inactive positions in the gap") and backed by implementation evidence (Gregory Q11/Q13), not a derivation. Implementation behavior is not a proof of a formal claim.
**Required**: Supply a concrete counterexample (e.g., `V_S(d) = {[S,1],[S,3]}` with `[S,2]` inactive) showing that the unique min-to-max span necessarily includes `[S,2] ∈ VSlice`, so `⟦span⟧ ∩ VSlice ⊋ V_S(d)`; or weaken W5 to the single direction the ASN actually uses.

### Issue 3: W9 is trivial as formalized; the substantive claim is grounded in implementation, not the foundation
**ASN-0113, W9**: "TwoKindsOnly — `occupied(d) ⊆ {s_C, s_L}`."
**Problem**: W6 *defines* `occupied(d) = {S ∈ {s_C, s_L} : V_S(d) ≠ ∅}`, so `occupied(d) ⊆ {s_C, s_L}` is true by construction — the formal statement carries no content. The intended substantive guarantee (no document content resides in a third subspace, so no third member can arise) is supported in the prose only by "Gregory's implementation confirms the architectural impossibility." That guarantee is already available in the foundation: S3★-aux (SubspaceExhaustiveness, ASN-0047) states `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`.
**Required**: Either restate W9 as the non-trivial fact (`O(d) = V_{s_C}(d) ⊔ V_{s_L}(d)`) and derive it from S3★-aux, or drop the implementation appeal and cite S3★-aux as the ground.

### Issue 4: No concrete worked example
**ASN-0113, throughout**: The note states W0–W19 abstractly but never instantiates the operation on a specific document.
**Problem**: The depth standard requires verifying key postconditions against at least one concrete scenario. There is no worked case (e.g., a document with 5 text positions and 2 links) checking that the result is `⟨([1,1], δ(5,2)), ([2,1], δ(2,2))⟩`, with W4 (exact coverage), W11 (disjointness), and W16 (partition) verified against it — including a degenerate `m_S = 2` instance where the canonical `[S,1,…,1]` form collapses.
**Required**: Add one concrete scenario verifying W3, W4, W11, W13, and W16.

## OUT_OF_SCOPE

### Topic 1: Behavior of the report under non-contiguous subspaces
**Why out of scope**: The first open question (fragmenting per cluster vs. single bounding span) describes a state the docuverse never reaches under D-CTG★; designing the fragmented report is future territory, not an error here. W5 only needs to *acknowledge* the dependency, which it does.

### Topic 2: Transclusion and version-fork interaction with reported extents
**Why out of scope**: The open questions on transclusion-from-an-edited-source and version-fork permanence belong with version comparison / transclusion semantics, which are excluded. W19's conditional stability statement is adequate for this ASN.

VERDICT: REVISE
