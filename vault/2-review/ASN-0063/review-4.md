# Review of ASN-0063

## REVISE

### Issue 1: K.μ⁺ not restricted to content subspace — S3★ preservation claim is unjustified

**ASN-0063, Extending the Transition Framework**: "Existing transitions (K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.ρ) trivially preserve S3★ because none creates link-subspace mappings: each either holds M in frame or extends/contracts only content-subspace positions, and the link-subspace clause is vacuously satisfied when no link-subspace V-positions exist."

**Problem**: K.μ⁺ (ASN-0047) has no subspace restriction on new V-positions. Its preconditions require `a ∈ dom(C)` for new mappings and S8a compliance for new V-positions, but nothing prevents creating a V-position with `subspace(v) = s_L` mapping to a content address `a ∈ dom(C)`. Since s_L ≥ 1 (as the ASN itself derives from T4), such a V-position satisfies S8a's range guard `v₁ ≥ 1` and all of K.μ⁺'s explicit preconditions. But the resulting mapping violates S3★, which requires link-subspace positions to map into `dom(L)`, not `dom(C)`. The claim that K.μ⁺ "extends only content-subspace positions" is asserted but not derivable from K.μ⁺'s definition.

**Required**: Add an explicit content-subspace restriction to K.μ⁺ for the extended state: "new V-positions satisfy `subspace(v) = s_C`." This parallels K.μ⁺_L's restriction to `subspace(v) = s_L` and makes the two transitions complementary. With this amendment, the S3★ preservation claim is justified: K.μ⁺ only creates content-subspace mappings targeting `dom(C)`, and K.μ⁺_L only creates link-subspace mappings targeting `dom(L)`.

### Issue 2: Extended initial state Σ₀ not defined

**ASN-0063, Extending the Transition Framework**: "The extended system state is Σ = (C, L, E, M, R), where L : T ⇀ Link is the link store (ASN-0043)."

**Problem**: The ASN extends the system state to include L but does not update the initial state definition. ASN-0047 defines Σ₀ = (C₀, E₀, M₀, R₀). The extended state requires Σ₀ = (C₀, L₀, E₀, M₀, R₀) with L₀ specified. Without this, the base case for the reachable-state invariants theorem is incomplete — we cannot verify that the extended invariants (S3★, P4★, L0–L14) hold at the initial state.

**Required**: Define the extended initial state: Σ₀ = (C₀, L₀, E₀, M₀, R₀) with L₀ = ∅. Verify that L₀ = ∅ satisfies the link invariants vacuously (L0, L1, L1a, L12, L14 all hold for empty L; S3★'s link-subspace clause is vacuous). This closes the inductive base for CL11's guarantees.

### Issue 3: K.μ⁺_L references undefined link-subspace depth m_L

**ASN-0063, K.μ⁺_L precondition**: "If V_{s_L}(d) = ∅: v_ℓ is the minimum position [s_L, 1, ..., 1] of depth m_L (D-MIN), where m_L is the link-subspace V-depth for d"

**Problem**: When V_{s_L}(d) = ∅, there is no "link-subspace V-depth for d" — no link-subspace V-positions exist from which to derive m_L. The precondition references a value that does not yet exist. When V_{s_L}(d) ≠ ∅, m_L is determined by the existing positions (S8-depth), but the first-link case is undefined.

**Required**: Specify that when V_{s_L}(d) = ∅, m_L is a parameter of the K.μ⁺_L transition (or of the CREATELINK composite), subject to the constraint m_L ≥ 2. When V_{s_L}(d) ≠ ∅, m_L is the common depth of existing link-subspace V-positions (determined by S8-depth). The CREATELINK precondition should state this explicitly: "m_L ≥ 2, chosen by the operation when V_{s_L}(d) = ∅, determined by S8-depth otherwise."

## OUT_OF_SCOPE

### Topic 1: Additional subspace types beyond s_C and s_L
**Why out of scope**: S3★ covers two subspaces. Future subspace types (if any) would need their own referential integrity clauses. This is new territory for a future ASN, not a gap in the current two-subspace framework.

### Topic 2: Link withdrawal operation
**Why out of scope**: The ASN discusses orphan links and notes that K.μ⁻ applied to the link subspace would produce them, but does not define a WITHDRAWLINK composite. A dedicated withdrawal operation with its own postconditions and invariant preservation proof belongs in a future ASN.

### Topic 3: Link transclusion across documents
**Why out of scope**: K.μ⁺_L's preconditions permit mapping a V-position to any link in dom(L), including links with origin(ℓ) ≠ d. This enables a document to include another document's out-links in its arrangement — a link analog of content transclusion. The semantics and invariants of cross-document link inclusion are not addressed and belong in a future ASN.

VERDICT: REVISE
