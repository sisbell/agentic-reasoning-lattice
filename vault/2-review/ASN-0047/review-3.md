# Review of ASN-0047

## REVISE

### Issue 1: Coupling constraints J0, J1, J1' are undefined for freshly created documents

**ASN-0047, Coupling and isolation**: J0 quantifies "d ∈ E_doc", J1 and J1' reference "ran(M(d))" — both presuppose d exists in the initial state.

**Problem**: For a freshly created document d_new ∈ E'_doc \ E_doc, M(d_new) is undefined (M's domain is E_doc from the initial state). This means:

- J0 cannot find d_new as the container for freshly allocated content, since d_new ∉ E_doc. The composite "K.δ (create document) + K.α (allocate content) + K.μ⁺ (place in new document) + K.ρ" — a fundamental operation — violates J0 as written, because the only document containing the new content is one that didn't exist in the initial state.
- J1's expression `ran(M'(d)) \ ran(M(d))` is undefined when d ∉ E_doc. Transclusion into a freshly created document has no coupling constraint requiring provenance recording.
- J1' has the same `ran(M(d))` reference and the same gap.

J4 handles the specific fork case (d_new ∈ E'_doc \ E_doc with no new content), but does not cover creating a new document with new content or transcluding existing content into a non-fork new document. The prose of J0 says "some arrangement" without restriction, but the formal statement restricts to E_doc (initial). These diverge.

This also affects the P4 proof: the K.μ⁺ case defines Δ = {(a, d) : a ∈ ran(M'(d)) \ ran(M(d))}, which is undefined for freshly created d.

**Required**: Either (a) quantify J0 over E'_doc and define the convention M(d) = ∅ for d ∈ E'_doc \ E_doc in J1/J1', or (b) introduce an explicit bridging rule for freshly created documents parallel to J4. The P4 proof should note the convention used.

### Issue 2: Foundation arrangement invariants not stated as transition constraints

**ASN-0047, Elementary transitions**: K.μ⁺ states "referential integrity requires a ∈ dom(C') (S3, ASN-0036)" but does not mention S8a, S8-depth, or S8-fin.

**Problem**: K.μ⁺ and K.μ~ modify arrangements but the ASN states no constraint requiring preservation of ASN-0036's arrangement invariants beyond S3. Concrete counterexample: document d has M(d) = {[1] ↦ a₁, [2] ↦ a₂} (V-positions at depth 1). K.μ⁺ adds [1,1] ↦ a₃. Now V-positions [1], [2] have depth 1 and [1,1] has depth 2 — violating S8-depth. Similarly, K.μ~ with a bijection π that maps V-positions to tumblers of different depth or with zero components violates S8-depth and S8a respectively. Nothing in the ASN prevents this.

The ASN selectively references foundation constraints (S3 for K.μ⁺, S7a/S7b for K.α, T4 for E, T8 for P1) but omits the arrangement structure invariants. Since S3 is mentioned, the omission of S8a and S8-depth reads as a gap, not a scoping choice.

**Required**: State that K.μ⁺ requires new V-positions to satisfy S8a and S8-depth, and that K.μ~ requires π to map to V-positions satisfying the same. A general note that all ASN-0036 invariants (S2, S3, S8a, S8-depth, S8-fin) must hold at the final state of every composite transition would also suffice.

### Issue 3: Missing cross-layer invariants

**ASN-0047, The state model / Temporal decomposition**: The existential layer (C, E) and historical layer (R) are described as separate but no formal invariant connects them.

**Problem**: Two invariants are derivable from the ASN's own definitions but not stated:

(a) **Existential coherence**: `(A a ∈ dom(C) :: origin(a) ∈ E_doc)`. K.α references S7a ("allocated under the creating document's prefix") and J0 requires placement in some arrangement (defined on E_doc), but no invariant ties origin(a) to an existing entity. Without this, content can have a structural attribution (S7) that points to a non-existent document.

(b) **Provenance grounding**: `(A (a, d) ∈ R :: a ∈ dom(C))`. K.ρ requires a ∈ dom(C) at recording time. P0 preserves dom(C). So the invariant holds in all reachable states by induction. But it is not stated, and the temporal decomposition's claim that the layers have distinct permanence contracts would be strengthened by noting this dependency: every R entry is grounded in the existential layer.

The ASN describes three temporal layers with distinct contracts. These invariants are the formal bridges between them — R doesn't just grow arbitrarily; it grows in lockstep with C and E. The derivation is straightforward (one step from K.ρ's precondition + P0/P1) but absent.

**Required**: State both invariants. Derive each from K.ρ's precondition and the relevant permanence property.

### Issue 4: No concrete worked example

**ASN-0047, throughout**: The ASN defines six elementary transitions, five coupling constraints, and proves P4 and P5. No scenario is traced through the model with specific addresses.

**Problem**: The fork discussion in J4 is the closest to a worked example, but it uses only set-theoretic notation, not specific tumblers or values. A scenario such as "document 1.0.1.0.1 with arrangement {[1] ↦ 1.0.1.0.1.0.1.1, [2] ↦ 1.0.1.0.1.0.1.2}; fork to 1.0.1.0.2" — traced through K.δ, K.μ⁺, K.ρ, and verified against P0–P5 and J0–J4 — would ground the abstract definitions and reveal any hidden assumptions in the transition model.

**Required**: Add at least one scenario (fork or insert-with-transclusion) with concrete tumbler addresses, verifying the key postconditions (P4 containment bound, P5 destruction confinement, J1 provenance coupling) against the result.

## OUT_OF_SCOPE

### Topic 1: System bootstrapping and initial state
**Why out of scope**: K.δ describes entity creation "via inc(·, k) under the parent's prefix," which assumes a pre-existing parent. The initial state Σ₀ = (∅, ∅, λd.⊥, ∅) admits no K.δ transitions (no parent to increment from). How root nodes come into existence — whether by a bootstrap primitive, a non-empty initial state, or an external mechanism — is a system initialization question, not a state transition question. The P4 proof's base case on the empty state is technically correct (vacuously satisfied), but a future ASN should define the initial reachable state.

### Topic 2: Entity creation hierarchy enforcement
**Why out of scope**: K.δ's formal specification (`E' = E ∪ {e}` where `e ∉ E`) does not require the parent entity (the prefix-truncated tumbler) to exist in E. A document could be created without its parent account existing. Whether the transition model should enforce hierarchical creation order (node before account before document) is an allocation discipline question that belongs with authority and ownership, not with the abstract transition taxonomy.

VERDICT: REVISE
