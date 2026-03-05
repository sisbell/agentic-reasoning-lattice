# Review of ASN-0013

## REVISE

### Issue 1: Writer Independence theorem is false as stated — COPY reads source POOM
**ASN-0013, Writer Independence theorem**: "The only authoritative state op₁ reads from outside wd(d₁) is I-space content — and I-space content is immutable (CΣ1), so op₂ cannot modify what op₁ reads."
**Problem**: COPY on document d₂ from document d₁ reads poom(d₁) to resolve source V-positions to I-addresses. A concurrent INSERT on d₁ writes poom(d₁). This is a read-write conflict on mutable authoritative state. The proof's claim that the only cross-boundary reads are on immutable I-space content is false.
**Required**: Acknowledge that cross-document operations (COPY, RETRIEVECONTENTS, and any operation that resolves V-positions in another document) read mutable authoritative state of the source document. The system handles this through CON5/CON8 (the reader sees a before-or-after snapshot), not through the absence of conflicts. The theorem should be restated: operations on different documents have no *write-write* conflicts; read-write conflicts exist but are resolved by snapshot isolation. The CON7 enumeration (which claims COPY "reads I-space addresses from d₁ — immutable by CΣ1") has the same error and must be corrected.

### Issue 2: CON1 scoped too narrowly
**ASN-0013, CON1**: "For documents d₁, d₂ under different accounts: alloc_range(d₁) ∩ alloc_range(d₂) = ∅"
**Problem**: Allocation ranges are determined by document tumbler prefixes, not account prefixes. Two documents under the *same* account (e.g., 1.1.1 and 1.1.2) have different document-level tumblers and thus disjoint allocation ranges by the same prefix-freeness argument. The "different accounts" qualifier is unnecessarily narrow and leaves a gap — the Writer Independence theorem depends on CON1 but is stated for all d₁ ≠ d₂, including same-account documents.
**Required**: State CON1 for all distinct documents d₁ ≠ d₂, not just those under different accounts. The justification (prefix-freeness of tumbler addresses) already supports the stronger statement.

### Issue 3: CON5 formalized for one concurrent mutation only
**ASN-0013, CON5**: "result(Q, observed_state) ∈ { result(Q, Σ₀), result(Q, Σ₁) }"
**Problem**: This formulation considers a single mutation M. When mutations M₁ on d₁ and M₂ on d₂ execute concurrently with query Q, the requirement is that Q observes a state consistent with some interleaving — e.g., (after M₁, before M₂) — but NOT a state where M₁'s effects on the global indexes are partially visible while M₂'s are fully visible. The binary formulation cannot express this multi-mutation consistency requirement.
**Required**: Generalize CON5 to state that every query observes a state equivalent to one reachable by applying some subset of completed mutations in some serializable order. For the single-server case this falls out of CON8 + sequential execution, but the abstract specification should state it for the general case.

### Issue 4: Content-location index (locidx) maintenance unspecified
**ASN-0013, CΣ4 and throughout**: CΣ4 is introduced and CON9(a) constrains it, but no property governs its maintenance.
**Problem**: The link index gets CON3 (append-only), which is central to the concurrency argument (CON4, CON7 enumeration, no-blocking corollary). The content-location index gets no equivalent property. Is locidx append-only? Is it updated on DELETE? Must it be updated atomically with the POOM? The ASN cannot claim that global-index concurrency is safe while leaving half the global indexes unspecified.
**Required**: State whether locidx is append-only (like linkidx), pruned on DELETE, or something else. If append-only, state the property analogous to CON3 and derive its consequences. If pruned, explain how pruning interacts with concurrent queries (a reader observing a half-pruned locidx would violate CON5).

### Issue 5: CON10 omits locidx
**ASN-0013, CON10**: "DELETE locality" specifies effects on poom, ispace, and linkidx. No mention of locidx.
**Problem**: DELETE removes V-positions from poom(d₁). If locidx is maintained, it must either be updated (removing d₁ from locidx entries for the deleted I-addresses) or left stale (over-approximation per CON9's ⊇). The ASN doesn't say which. Since locidx is defined in CΣ4 as part of the state model, CON10 should specify DELETE's effect on it.
**Required**: Add a part (e) to CON10 stating DELETE's effect on locidx. If locidx is append-only, state Σ'.locidx = Σ.locidx explicitly. If it's pruned, specify the update.

### Issue 6: CREATENEWVERSION described as creating a document
**ASN-0013, CON7 enumeration**: "Version creation (CREATENEWVERSION). Reads the source document's arrangement mapping and creates a new document with the same content references."
**Problem**: CREATENEWVERSION creates a new *version* within the same document, not a new document. Versions share the document's tumbler prefix (node.user.document.version). The new version has its own POOM but is within the same document identity. This mischaracterization matters: if it created a new document, CON0 would apply between old and new; since it creates a version within the same document, it falls under per-document ordering and does not belong in the cross-document interaction enumeration at all.
**Required**: Correct "creates a new document" to "creates a new version." If this operation is cross-document in some sense (reading from one document to create a version in another), explain how. If it's within-document only, remove it from the cross-document enumeration or explain why it's listed there.

### Issue 7: No concrete example
**ASN-0013, throughout**: The ASN introduces 17 properties and several theorems without a single concrete scenario.
**Problem**: A concurrency specification that never traces a specific concurrent execution is untested against its own definitions. The review instructions require at least one specific scenario that exercises the key postconditions.
**Required**: Trace a scenario such as: User A performs INSERT 'XY' at position 3 in document D₁ while User B performs CREATELINK in document D₂ with an endset referencing I-space addresses shared with D₁ through transclusion. Show: (a) what state components each operation touches, (b) that the write domains are disjoint at the authoritative level, (c) that the link index update from B's CREATELINK is discoverable from D₁ after B's operation completes, (d) that CON5 is satisfied for a query concurrent with both operations.

### Issue 8: CΣ3/CΣ4 derivability claim is ambiguous
**ASN-0013, State model**: "Both CΣ3 and CΣ4 are derived state — they can be computed from the arrangement mappings and the link store"
**Problem**: CΣ3 (link index) is derived from the link store (a subset of I-space), not from arrangement mappings. CΣ4 (content-location index) is derived from arrangement mappings, not from the link store. The sentence attributes both to the union of sources, which is imprecise and obscures which index depends on which authoritative state — a distinction that matters for the concurrency argument.
**Required**: State the derivation source for each index separately: CΣ3 is derived from the link structures in I-space; CΣ4 is derived from the arrangement mappings.

### Issue 9: Derivability section lists CON5 and CON8 as both "truly axiomatic"
**ASN-0013, Derivability**: "Of these, the truly axiomatic properties... are CΣ1, CON5, and CON8."
**Problem**: The ASN itself says "CON8 is stronger than CON5" and the derivability section notes CON8 "implies CON5 for single-server." If CON5 is derivable from CON8 in the single-server case, they are not independent. For the multi-server case, they may be independent, but the ASN doesn't make this distinction in the derivability analysis. The claim of three independent axioms contradicts the stated derivability relationship.
**Required**: Either: (a) state that CON5 is the axiom and CON8 is a strengthening (making CON8 derivable from CON5 + mechanism), or (b) state that CON8 is the axiom and CON5 is a theorem for single-server, promoted to axiom for multi-server, or (c) clarify the exact scope under which both are independent.

## OUT_OF_SCOPE

### Topic 1: Information-flow consequences of globally discoverable links
**Why defer**: CON6 establishes that link queries bypass per-document access control. This means a link created in a private document with endsets referencing shared content becomes discoverable by anyone who transcludes that content. Whether this constitutes an information leak — and whether the specification should constrain it — is a policy question beyond this ASN's scope.

### Topic 2: Multi-server convergence guarantees
**Why defer**: The ASN correctly notes Nelson's "subrepresentation model" and raises BEBE replication in the open questions. The convergence semantics for replicated global indexes (eventual consistency, causal consistency, bounded staleness) are a separate specification concern. This ASN establishes the single-server properties; distributed semantics belong in a dedicated ASN.

### Topic 3: COPY as a two-document operation
**Why defer**: Issue 1 identifies the gap, but fully resolving it may require a new classification of operations: single-document (INSERT, DELETE) vs. cross-document (COPY, possibly CREATELINK with cross-document endsets). This classification and its implications for the concurrency model may warrant its own ASN rather than a patch to this one.