# Review of ASN-0047

## REVISE

### Issue 1: Ghost-base versioning is admitted without design rationale

**ASN-0047, K.δ Per-sub-case additional requirements (k = 1 version) and Worked example: ghost-base document versioning**: "k = 1 (version): IsDocument(t). The operand need not be in E_doc; when t ∉ E_doc (ghost-base versioning) the freshness discharge routes through direct E-inspection rather than T10a GlobalUniqueness".

**Problem**: The ASN admits the ghost-base case (an inc operand t that is IsDocument but not in E_doc), but does not justify why. The only rationale given — "matching Gregory's implementation which has no state representation for structurally valid but uninstantiated tumblers" — is implementation-driven, not design-driven. This is a load-bearing choice: it forces the S7d→S7d★ relaxation, requires a separate freshness-discharge route (direct E-inspection), and opens a concurrency concern flagged in Open Questions. Nelson's design intent and the abstract motivation are absent.

**Required**: Either (a) cite the design source for ghost-base versioning in Nelson's specification and state the use case it serves, or (b) restrict K.δ k = 1 to require t ∈ E_doc, eliminating the ghost-base case along with S7d★ and the direct-inspection discharge route.

### Issue 2: Foundation invariant S7d weakened to S7d★ without prominent flagging

**ASN-0047, Local extensions table entry for S7d★**: "Document allocation discipline (relaxed): every d ∈ E_doc is T4-valid with zeros(d) = 2, placed in E_doc by a K.δ event satisfying e ∉ E — discharged either by T10a GlobalUniqueness on a tracked allocator chain or by direct E-inspection at the K.δ event (ghost-base k = 1 sub-case)".

**Problem**: This is a substantive weakening of ASN-0036's S7d, which requires every document to result from a T10a allocation event. The relaxation is buried in a table near the end of the ASN. A reader inheriting the foundation invariant landscape would not realize that S7d no longer holds. The relaxation deserves prominent introduction near the K.δ definition (where the ghost-base sub-case is introduced), not at the back of the document.

**Required**: Add an explicit statement near the K.δ definition that ghost-base versioning weakens ASN-0036's S7d to S7d★. State the consequence (S7d's T10a-grounded uniqueness is replaced by either-T10a-or-direct-inspection uniqueness) and where in the proof structure each route applies.

### Issue 3: P5 introduced before P3, but P3 supersedes P5

**ASN-0047, "Destruction confinement" section (introduces P5) and "Extended monotonicity invariants" section (introduces P3 as superseding P5)**: P5 (Destruction Confinement) is introduced at the four-component state. Later, P3 (ArrangementMutabilityOnly) is introduced in the extended state and the text states "P3 supersedes P5 in the extended state by adding the L clause".

**Problem**: A reader following the document sequentially internalizes P5 first, then must replace it with P3 — a label that comes earlier in numbering but later in the document. The labels are confusingly assigned and the supersession is presentation-driven rather than principled.

**Required**: Either rename so supersession follows label order (e.g., merge P5 into P3 with a single per-transition statement), or eliminate P5 entirely by introducing P3 at first use.

### Issue 4: K.μ~ "zero elementary steps" expansion is semantically awkward

**ASN-0047, Decomposition of K.μ~**: "When π = id (including the empty bijection and the degenerate case dom_C(M(d)) = ∅, which forces π = id by link-subspace fixity), K.μ~ expands into zero elementary steps: M'(d) = M(d) and no K.μ⁻ + K.μ⁺ round-trip is invoked."

**Problem**: A "transition" that expands into zero elementary steps is not a transition — it is a no-op. The ASN treats K.μ~ as a uniform "named composite" with admissibility constraints and a frame, but its semantics is conditional: a real composite when π ≠ id, the identity when π = id. ValidComposite★'s clause (1) treats K.μ~ as "shorthand for its decomposition" while admitting the zero-step expansion, creating an ambiguity about whether a K.μ~ no-op contributes a "step" to the sequence.

**Required**: Either restrict K.μ~'s precondition to require π ≠ id (so K.μ~ is always a real K.μ⁻ + K.μ⁺ pair), or restructure the K.μ~ definition to acknowledge the degenerate case as a distinct admissibility regime ("K.μ~ trivially applies when π = id with no state change; otherwise K.μ~ decomposes as K.μ⁻ + K.μ⁺ with the constraints below").

### Issue 5: D-SEQ★ derivation cites S8-depth for shared first component

**ASN-0047, D-SEQ★ derivation, Step 1 base case**: "Every v ∈ V_S(d) has the form [S, v_2] with v_1 = S (from D-MIN★'s minimum position witness having v_1 = S, and S8-depth uniformity giving every v in the subspace the same first component) and v_2 ∈ ℕ⁺ (from S8a)".

**Problem**: S8-depth establishes uniform *depth* (#v) within a subspace, not a uniform first component. The shared first component v_1 = S follows from the definition of V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} and the projection subspace(v) = v_1 — every member of V_S(d) has v_1 = S by definition of the partitioning. Citing S8-depth for this is misleading and weakens the derivation.

**Required**: Replace the S8-depth citation with the definition of V_S(d) and the subspace projection. The corrected reading is: "v_1 = S by definition of V_S(d) (which projects M(d) onto positions with subspace(v) = S = v_1)".

### Issue 6: K.α cross-document distinctness omitted from the freshness-discharge summary table

**ASN-0047, Freshness-discharge summary table**: The table lists K.λ's "Cross-document distinctness" row via the Cross-document disjointness chain lemma, but no analogous row exists for K.α.

**Problem**: Two K.α events allocating under distinct documents must produce distinct addresses; the discharge is parallel to K.λ's (the Cross-document disjointness chain lemma applied with b_C in place of b_L). The Foundation invariants prose mentions this in passing, but the freshness-discharge summary table — presented as a comprehensive catalog — is incomplete for K.α. A reader using the table as a reference would not find K.α's cross-document discharge.

**Required**: Add a K.α cross-document distinctness row to the freshness-discharge summary table, citing the Cross-document disjointness chain lemma applied at the content-allocator anchors.

### Issue 7: Reviser drift in axiom prose — use-site enumeration

**ASN-0047, NodeUniqueAllocation axiom**: "Clause (b) supplies K.δ case (i)'s `n₀ ≼ e` precondition directly from the registry's issuing discipline, so the NodeLineage invariant — `(A e ∈ E : IsNode(e) : n₀ ≼ e)` — is inductively preserved by every K.δ node-allocation event."

**Problem**: The axiom's content is its two clauses (freshness + bootstrap lineage). The trailing sentence enumerates downstream consumers (K.δ case (i), NodeLineage) rather than advancing the axiom's meaning. This is the use-site-inventory pattern flagged in the rubric's reviser-drift list. Similar prose appears in LinkVPositionDepthAxiom ("supplying the depth in the empty-subspace case at K.μ⁺_L where S8-depth is vacuous") and in SubAllocatorAxiom ("T10a.6 non-violation" paragraph).

**Required**: Trim the consumer-enumeration prose. The axiom stands on its content; downstream consumption is visible at each use site.

## OUT_OF_SCOPE

### Topic 1: Link-withdrawal mechanism (tombstoning)

**Why out of scope**: The *Link-withdrawal gap under D-CTG★ / D-MIN★* paragraph identifies that Nelson's tombstoning design (LM 4/9) is not expressible as any K.μ⁻ transition or composite under the amended invariants. Reconciling this requires a separate withdrawal mechanism (status flag, tombstone marker, or explicit retraction link) operating outside K.μ⁻'s contract. This is correctly noted in Open Questions; a future ASN on operation semantics or withdrawal discipline should address it.

### Topic 2: Concurrent K.δ ghost-base discipline

**Why out of scope**: The Open Questions section asks what additional discipline beyond SequentialTransitionAxiom must hold to maintain soundness of K.δ's direct-E-inspection freshness discharge under concurrent allocation. This is implementation discipline, not abstract state structure. A future ASN on concurrency or operational protocol should address it.

### Topic 3: Node-allocation registry implementation

**Why out of scope**: NodeUniqueAllocation is treated axiomatically, with implementation details (issuing protocol, persistence model, concurrency discipline) explicitly deferred. The abstract specification stops at the axiom boundary; a future ASN on the node-allocation registry would extend it.

### Topic 4: Account-level depth-1 tumbler extension

**Why out of scope**: The Open Questions section asks whether K.δ k = 1 should admit IsAccount(t) (versioning at the account level). The current ASN excludes this with citation to Nelson and Gregory. Future address-space design extensions can revisit this.

### Topic 5: Forked document arrangement invariants relative to source

**Why out of scope**: The Open Questions section asks what invariants must hold between a forked document's initial arrangement and its source's current arrangement (identical, proper subset, or other). J4 as defined admits both full and partial transclusion at fork time; tightening this is a future design decision.

VERDICT: REVISE
