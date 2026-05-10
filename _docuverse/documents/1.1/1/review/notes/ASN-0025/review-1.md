# Review of ASN-0025

## REVISE

### Issue 1: J0 preservation never verified
**ASN-0025, State Model / Operations Under Permanence**: "J0: (A d ∈ Σ.D : rng(Σ.v(d)) ⊆ Σ.A)"
**Problem**: J0 is introduced as a well-formedness invariant, then never mentioned again. None of the six operation sections verify that J0 is preserved. INSERT adds new V-space entries pointing to freshly allocated B — J0 holds because B ⊆ Σ'.A, but this is not stated. COPY adds V-space entries pointing to S ⊆ Σ.A = Σ'.A — also not stated. CREATE VERSION creates a new document whose V-space mirrors an existing one — J0 for d' follows from J0 for d and P0, but this is not shown.
**Required**: Each operation section should include a one-line verification that J0 is preserved. The arguments are straightforward; they just need to be present.

### Issue 2: COPY V-space postcondition incomplete
**ASN-0025, COPY (Transclusion)**: "New V-positions map to *the same I-addresses* as the source content."
**Problem**: P5 establishes that source I-addresses become visible in target document d. The section says nothing about what happens to d's existing V-space entries. INSERT explicitly addresses this: "All V-positions at or beyond p shift forward by width n. The I-addresses of the shifted entries are unchanged." COPY is structurally similar — it inserts content into a V-space at some position, requiring existing entries to shift — but omits the corresponding statement. The reader cannot determine whether existing content in d is preserved, shifted, or silently dropped.
**Required**: State the V-space effect on existing entries in d explicitly, parallel to INSERT. At minimum: existing V-positions shift to accommodate the transcluded span; their I-address mappings are unchanged.

### Issue 3: No concrete worked example
**ASN-0025, throughout**
**Problem**: Every invariant preservation proof is purely abstract. The review standard requires at least one specific scenario verified against key postconditions. For example: document d with V-space {1↦a, 2↦b, 3↦c} undergoes INSERT of byte β at position 2 — trace through P0 (Σ.A grows by one), P1 (ι(a), ι(b), ι(c) unchanged), J0 (new entry points to allocated address), and the V-space shift. This would ground the abstract claims and catch any implicit assumptions about how the state model works.
**Required**: Add one concrete scenario (INSERT is the natural choice since it exercises both I-space and V-space) and verify P0, P1, J0, and the V-space postconditions against it.

### Issue 4: P9 references state outside the model
**ASN-0025, The Provenance Witness**: "P9 (Provenance Monotonicity). Spanfilade DOCISPAN entries are append-only."
**Problem**: The state model Σ has three components: Σ.ι, Σ.A, Σ.v. The spanfilade is not among them. P9 asserts an invariant over a structure that does not exist in the formal model, yet the Properties Introduced table lists P9 alongside P0–P8 as if it were a model property. A property cannot be formally maintained if the state it governs is not formally represented.
**Required**: Either (a) add the spanfilade to Σ (e.g., Σ.s : ISpan → DocId) and verify P9 for each operation, or (b) clearly demarcate P9 as an implementation observation — move it out of the properties table and into a separate "Implementation Evidence" subsection.

### Issue 5: CREATE VERSION I-space effect is self-contradictory
**ASN-0025, CREATE VERSION**: "I-space effect. None (aside from the version's own structural orgl entry)."
**Problem**: If CREATE VERSION allocates an orgl entry, the I-space effect is not "None." The parenthetical contradicts the claim it modifies. This also means CREATE VERSION should be listed alongside INSERT and CREATE LINK as an I-space-extending operation, but P3's exception list ("with the sole exceptions of INSERT and CREATE LINK") omits it.
**Required**: State the I-space effect directly: "CREATE VERSION allocates a structural entry (orgl) at a fresh I-address. Σ'.A = Σ.A ∪ {orgl_addr}." Add CREATE VERSION to P3's exception list.

### Issue 6: P3 conflates two distinct claims under one label
**ASN-0025, Visibility and Indestructibility**: "P3 (Indestructibility). No operation removes content from I-space."
**Problem**: The prose says "no operation removes content" — this is P0. The formal statement says "Σ'.A = Σ.A ∧ Σ'.ι = Σ.ι (with sole exceptions...)" — this is stronger than P0; it asserts non-extension for specific operations. The label "Indestructibility" matches the prose (P0) but not the formal statement (non-extension). Two distinct properties — "I-space never shrinks" and "these specific operations don't extend I-space either" — are merged into a single label, making it unclear which property is being invoked when P3 is referenced later.
**Required**: Either split into two properties (P3a: indestructibility = P0 restated for emphasis; P3b: non-extension for DELETE/REARRANGE/COPY) or rename P3 to reflect its formal statement and note that indestructibility is already captured by P0.

### Issue 7: Operation preconditions never stated
**ASN-0025, Operations Under Permanence**: all six operation sections
**Problem**: No operation lists its preconditions formally. INSERT requires d ∈ Σ.D, a valid insertion position, and allocator availability. COPY requires source I-addresses S ⊆ Σ.A and d ∈ Σ.D. DELETE requires the target span to exist in Σ.v(d). CREATE VERSION requires d ∈ Σ.D. The invariant preservation proofs implicitly assume these preconditions hold — for instance, COPY's J0 preservation depends on S ⊆ Σ.A — but without stating them, the proofs are technically incomplete: we cannot tell what conditions are assumed versus what conditions are established.
**Required**: State preconditions explicitly for each operation. They can be brief (one or two lines each). The non-trivial case is COPY, where S ⊆ Σ.A is essential and not guaranteed by the operation's description alone.

### Issue 8: P6 presented as independent but is a direct consequence of UF-V
**ASN-0025, CREATE VERSION**: "P6 (Version Independence). (A d₁, d₂ : ... any edit to Σ.v(d₁) leaves Σ.v(d₂) unchanged)"
**Problem**: Every operation in the ASN targets a single document d. UF-V states that operations on d leave Σ.v(d') unchanged for d' ≠ d. P6 states the same thing with different variable names. Presenting P6 as an independent property in the Properties Introduced table, alongside genuinely new properties like P0 and P1, overstates its novelty. A reader may look for what P6 adds beyond UF-V and find nothing.
**Required**: Present P6 as a derived consequence of UF-V applied across all operations, not as an independently introduced property. One sentence suffices: "Version independence follows from UF-V: since every editing operation targets a single document, no edit to one version's V-space can affect another's."

### Issue 9: P10 blurs the boundary between abstract model and implementation
**ASN-0025, The Durability Boundary**: "P10 (Committed Permanence). P0 ∧ P1 hold unconditionally over the sequence of *committed* (durably persisted) states."
**Problem**: The abstract model defines state transitions Σ → Σ'. P0 and P1 are invariants of those transitions — they apply to every step. P10 weakens this to "committed" states, introducing an implementation concept (disk flush, crash recovery, session boundaries) that does not exist in the abstract model. Listing P10 alongside P0–P9 in the properties table suggests it is part of the specification, but the ASN itself says "A conforming implementation providing operation-level durability would satisfy P0 ∧ P1 without the committed/tentative distinction." If an implementation can satisfy P0 ∧ P1 directly, P10 is not a specification requirement — it is an implementation note about a specific prototype.
**Required**: Move P10 out of the properties table. Keep the Durability Boundary section as implementation commentary but label it clearly: the abstract specification requires P0 ∧ P1 per-transition; P10 documents a known limitation of one implementation, not a property of the model.

## OUT_OF_SCOPE

### Topic 1: Link deletion and modification operations
**Why out of scope**: The ASN analyzes six operations (INSERT, DELETE, REARRANGE, COPY, CREATE VERSION, CREATE LINK) but does not analyze link deletion or modification. These belong in a links ASN that defines link lifecycle operations, their subspace interactions, and their permanence constraints.

### Topic 2: V-space ordering semantics for COPY and REARRANGE
**Why out of scope**: P5 guarantees visibility but not order; P4 guarantees multiset preservation but not the specific permutation. The full V-space ordering semantics — how content is arranged after transclusion or rearrangement — belongs in a V-space operations ASN, not in this permanence ASN.

### Topic 3: Historical backtrack and invisible content resolution
**Why out of scope**: The ASN correctly notes in Open Questions that content can become invisible in all documents while persisting in I-space. Whether the system must provide a mechanism to make such content visible again, and what "resolution" means for invisible content, are genuine specification questions — but they extend beyond permanence into system functionality.

VERDICT: REVISE
