# Review of ASN-0009

## REVISE

### Issue 1: VER1 does not specify what it claims to specify
**ASN-0009, VER1**: "img(d'.vmap) = img(d.vmap|text)"
**Problem**: Image equality constrains which I-addresses appear, not the arrangement. A compliant implementation could deduplicate (if 'a' appears at 3 positions in the source, map it once in the version), scramble the reading order, or pad with repetitions — and still satisfy VER1. The ASN says "The version shares content identity," and image equality suffices for that narrow claim. But the same section also says this is "the property that makes versioning meaningful," and a version with scrambled, deduplicated text is not meaningful as a version. The ASN needs either:
- (a) An arrangement-isomorphism postcondition: d'.vmap is order-isomorphic to d.vmap|text (same domain structure, same I-address at each corresponding position), or
- (b) An explicit acknowledgment that VER1 is the identity-level property and a separate structural postcondition is needed.
**Required**: Replace or supplement VER1 with a postcondition that constrains the arrangement, not just its image. VER6 attempts this but is too weak (see Issue 2).

### Issue 2: VER6 is one-directional
**ASN-0009, VER6**: "(A v : v ∈ dom(d.vmap|text) : (E v' : v' ∈ dom(d'.vmap) : correspond(d, v, d', v')))"
**Problem**: This says every source position has a correspondent in the version. It does not state the converse: every position in d' corresponds to some position in d. Without the converse, d' could contain positions mapping to I-addresses that are in img(d.vmap|text) — satisfying VER1 — but at positions that duplicate content arbitrarily. Together, VER1 and VER6 give surjectivity from source to version at the I-address level, but say nothing about injectivity or ordering.
**Required**: State the converse: (A v' : v' ∈ dom(d'.vmap) : (E v : v ∈ dom(d.vmap|text) : correspond(d, v, d', v'))). Better yet, fix VER1 per Issue 1, which makes VER6 a corollary rather than a patch.

### Issue 3: Link subspace prefix
**ASN-0009, State Components**: "the link subspace (positions prefixed 2.x)"
**Problem**: The shared vocabulary and the EWD framework consistently use 0.x for the link subspace within a document (1.x for text, 0.x for links). The ASN uses 2.x without justification.
**Required**: Change "2.x" to "0.x" or explicitly define and justify the departure from the established convention.

### Issue 4: VER-ISO proof rests on an unstated axiom
**ASN-0009, Version Isolation**: "Every editing operation takes a document identifier as an explicit argument and locates that document's arrangement by its address. The operation then modifies only the located arrangement."
**Problem**: This "operation scoping" property is the load-bearing premise. It is asserted, not established. The ASN should either (a) state it as an axiom (which it effectively is), or (b) derive it from the operation definitions. The current proof structure is: assume scoping, observe address distinctness, conclude isolation. The assumption is doing all the work and is invisible in the formal property list. Additionally, COPY reads a source document and writes to a target — it touches two documents. The scoping claim should be stated precisely: each operation *writes* to exactly one document's arrangement.
**Required**: State operation scoping as a named property in the Properties table. Clarify that it means "writes to exactly one arrangement" since some operations read from others.

### Issue 5: VER3 uses undefined relation
**ASN-0009, VER3**: "d'.addr is a sub-address of d.addr"
**Problem**: "Sub-address" is not defined anywhere in this ASN or in the shared vocabulary. It presumably means that d'.addr has d.addr as a proper prefix, but this is never stated. The ASN then immediately undercuts the relation by quoting Nelson saying address placement "does not entail derivation logically." If sub-address is a purely conventional property with no formal content, VER3 should say so. If it IS formal (prefix relationship on tumblers), it should be defined.
**Required**: Define "sub-address" formally (prefix, extension, or whatever it means), or relabel VER3 as a convention rather than a postcondition.

### Issue 6: VER11 is not formalizable as stated and contradicts VER3
**ASN-0009, VER11**: "no system property distinguishes d₁ from d₂ as 'primary'"
**Problem**: "No system property distinguishes" is informal to the point of being unformalizable. VER3 provides exactly such a distinguishing property — the parent has a shorter address than the child. Address length is a computable system quantity. Creation order is a system fact. Ownership may differ. What VER11 means is something narrower: no operation treats one version as canonical (e.g., no operation takes a "primary version" argument). But that is a claim about the operation set, not a universally quantified statement about system properties.
**Required**: Either formalize VER11 precisely (e.g., "no operation's precondition or postcondition references a 'primary version' designator") or demote it to a design principle stated in prose.

### Issue 7: VER16 is tautological
**ASN-0009, VER16**: "a ∈ img(d₁.vmap) ∧ a ∈ img(d₂.vmap) ⟹ d₁ and d₂ share content identity at a"
**Problem**: "Share content identity at a" means, by the definitions in this ASN, that both documents' arrangements map some position to I-address a. The premise states exactly this. The conclusion is a restatement of the premise in different words. The surrounding prose claims transitivity through "chains of versioning and transclusion," but the property itself makes no reference to chains — it's a direct consequence of img membership. What would be non-trivial: showing that specific chains of operations (version of version, transclusion from version, etc.) produce the shared-image-membership condition. That derivation is absent.
**Required**: Either derive the claim for specific operation chains (e.g., "if d₂ = version(d₁) and d₃ = version(d₂), then img(d₁.vmap|text) ⊇ img(d₃.vmap) at creation time"), or remove VER16 and state the observation informally.

### Issue 8: parent() is not in the state model
**ASN-0009, Definition ANC**: "parent : DocId → DocId ∪ {⊥}, where parent(d') = d when d' was created by CREATENEWVERSION(d, u)"
**Problem**: The state model in "State Components" lists d.addr, d.vmap, d.links, d.owner for documents, and Σ.docs, Σ.ispace, etc. for the system. The parent relation appears nowhere. ANC defines it as tracking "when d' was created by CREATENEWVERSION" — but creation history is not a state component. VER13 (ancestry permanence) then asserts parent() is permanent, but permanence of what? If parent() is derived from address structure (VER3), say so explicitly and derive VER13 from address permanence. If it is a separate state component, add it to the state model and specify that CREATENEWVERSION establishes it (postcondition) and nothing else modifies it (frame condition).
**Required**: Either add parent to the state model with appropriate postcondition and frame conditions, or explicitly derive it from d.addr and define "sub-address."

### Issue 9: VER12 formalization incomplete
**ASN-0009, VER12**: Gives two conditions: parent points to existing document or ⊥, and acyclicity.
**Problem**: The prose says "parent is a partial function (each document has at most one parent)" but the formalization omits the function property. The two stated conditions are consistent with parent being a relation (multiple parents). Additionally, the acyclicity proof ("d' was created after d, and no backward edge can arise") is a temporal argument that relies on the system being single-threaded or at least having a total order on document creation — which is true but unstated in this ASN.
**Required**: Add the function property to the formalization: parent(d) is uniquely defined for each d. Either state the single-threaded assumption or prove acyclicity without it.

### Issue 10: COR span extension assumes contiguous I-addresses
**ASN-0009, COR extension**: "contiguous positions [v₁, v₁ + w) in d₁ correspond to [v₂, v₂ + w) in d₂ when both map to the same contiguous I-address range [a, a + w)"
**Problem**: After editing operations, contiguous V-positions routinely map to non-contiguous I-addresses (an INSERT in the middle of a span splits its I-address continuity). The "contiguous I-address range" requirement means span correspondence fails at every edit boundary, even when the individual-position correspondence still holds. This makes the span extension nearly useless for post-edit analysis while the pointwise COR definition works fine.
**Required**: Acknowledge this limitation, or define span correspondence as pointwise-for-all-positions rather than requiring I-address contiguity.

### Issue 11: VER15 is redundant with VER-F2
**ASN-0009, VER15**: "Σ'.alloc = Σ.alloc"
**Problem**: VER-F2 already states "Σ'.alloc = Σ.alloc" as a frame condition. VER15 restates it. The Properties table lists both, inflating the property count. Redundancy in a formal specification invites inconsistency during revision.
**Required**: Remove VER15 or note it as "= VER-F2" in the Properties table. Do not list the same property twice under different names.

## OUT_OF_SCOPE

### Topic 1: Interaction with AUTH/BERT
PRE-VER says "any user may version any document." The authorization model (AUTH0-AUTH5, BERT modes) specifies when versioning is triggered automatically vs. when modification proceeds. This is protocol-level, not state-transition-level; a future ASN on authorization/versioning interaction would address it.
**Why defer**: PRE-VER specifies the operation's precondition. When and why the operation is invoked is a separate concern.

### Topic 2: Version creation under concurrent access
The isolation theorem and acyclicity proof both assume sequential execution. Concurrent version creation (two users versioning the same document simultaneously) is deferred to the concurrency model.
**Why defer**: The ASN explicitly builds on a sequential model. Concurrent semantics belong in a concurrency ASN.

### Topic 3: Transcluded content across permission boundaries
The first open question (versioning when the source contains transcluded content the user cannot read) is genuine and important but requires the authorization model to be fully specified first.
**Why defer**: Requires AUTH framework not yet covered in ASN series.