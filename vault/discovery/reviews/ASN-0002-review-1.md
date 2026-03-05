# Review of ASN-0002

## REVISE

### Issue 1: INSERT preservation proof is circular
**ASN-0002, Operation-by-operation analysis / INSERT**: "And for all pre-existing addresses: `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` by AP1 (content immutability)."
**Problem**: AP1 *is* the claim that content at existing addresses never changes. Citing AP1 to establish that INSERT preserves AP1 is circular. The justification must come from the operation's mechanics: INSERT writes only to freshly allocated addresses; those addresses are disjoint from dom.ispace (by the freshness constraint); therefore no existing ispace entry is modified. The ingredients are present (AP2/freshness is cited one line above), but the logical connective is wrong — AP2 is the reason, not AP1.
**Required**: Replace "by AP1" with a derivation from the operation's effect: INSERT writes only at fresh addresses disjoint from dom.ispace, so no pre-existing entry is read or written. State separately that dom.ispace ⊆ dom.ispace' (AP0 preservation) because INSERT extends ispace and contains no removal instruction. The same circularity recurs in the theorem proof — "AP0 and AP1 hold" is the conclusion, not a reason. Derive each from the operation's specified effect.

### Issue 2: Theorem quantifies over all operations but the set is not closed
**ASN-0002, Theorem (Address-content invariance)**: "For every reachable state Σ and every operation transforming Σ to Σ'"
**Problem**: The proof covers six operations: INSERT, DELETE, REARRANGE, COPY, CREATENEWVERSION, CREATELINK. But the theorem claims to hold for *every* operation. Document creation (as distinct from version creation), account creation, node creation, and any administrative operations are not addressed. The proof is valid only if these six operations are the complete set, but the ASN never declares this.
**Required**: Either (a) state explicitly that these six operations are the complete set of operations that modify Σ, or (b) weaken the theorem to "for every operation defined in this ASN" and note that future operations must be shown to preserve AP as a condition of their introduction.

### Issue 3: Span index forward correspondence asserted but never verified
**ASN-0002, The historical index**: "`(A d, a : (E p : vspace(d).p = a) ⟹ (a, d) ∈ spanindex)` Every live reference is indexed."
**Problem**: This is stated as a system invariant but no operation's analysis shows that it is maintained. INSERT creates new vspace entries — does it add spanindex records? COPY creates new vspace entries in the target — does it update spanindex? CREATENEWVERSION creates new vspace entries — does it update spanindex? The operation-by-operation analysis mentions spanindex only once (DELETE doesn't remove entries), and never specifies which operations *add* to it. The forward correspondence is a claim without proof.
**Required**: For each operation that creates or modifies vspace entries, state its effect on spanindex and verify that the forward correspondence is preserved. Alternatively, if spanindex maintenance is deferred to a future ASN, remove the forward correspondence claim and mark it as an open question.

### Issue 4: AP13 discoverability depends on undefined mechanism
**ASN-0002, Link survivability as consequence**: "The link is discoverable after re-transclusion because the span index still records the link's association with those I-addresses"
**Problem**: The span index is defined as `spanindex ⊆ Addr × DocId` — it records which documents have contained which addresses. It does not record which *links* are associated with which content addresses. The claim that spanindex enables link discovery requires a lookup from content I-addresses to links, but no such mechanism is defined. How does the system find links whose endsets contain a given I-address? The enfilade vocabulary mentions a "link enfilade" for this purpose, but this ASN neither introduces it nor provides an alternative.
**Required**: Either (a) define the mechanism by which links are discovered given content I-addresses and show it survives the re-transclusion scenario, or (b) weaken AP13 to state only that the link's endset references remain valid (which follows from AP1) and defer the discoverability claim to an ASN that defines the link-discovery mechanism.

### Issue 5: CREATENEWVERSION document address is neither in nor out of dom.ispace
**ASN-0002, CREATENEWVERSION**: "CREATENEWVERSION allocates one fresh address — the new document's identity. It does NOT allocate new content addresses."
**Problem**: The document identity address is "allocated" but the ASN does not state whether it enters dom.ispace. If it does, then ispace maps it to some content (what content?), and the theorem proof must verify AP0 and AP1 for it specifically. If it does not, then it is not governed by AP0–AP4 and lives in an unspecified part of the system state. The theorem proof mentions "Allocates one fresh document address" but draws no conclusion from it — it neither includes nor excludes this address from the ispace analysis.
**Required**: State explicitly whether the document identity address enters dom.ispace. If yes, specify what content it maps to and verify AP in the theorem. If no, specify where it is recorded and what permanence properties, if any, apply to it (this is already noted in the Open Questions but the theorem proof cannot be silent on it).

### Issue 6: COPY frame condition is contradictory when source equals target
**ASN-0002, COPY / Frame conditions**: "COPY modifies `vspace(d₂)` (the target) but not `vspace(d₁)` (the source). The source document is a read-only participant."
**Problem**: If d₁ = d₂ (COPY within the same document), this states that COPY both modifies and does not modify vspace(d₁) — a contradiction. The I-space permanence properties are unaffected (COPY never touches ispace regardless), but the V-space frame condition as written is false for self-copy. AP14 correctly qualifies with d₂ ≠ d₁, but the COPY section's own frame condition does not.
**Required**: Add a qualifier: "For d₁ ≠ d₂, COPY does not modify vspace(d₁)" or handle the d₁ = d₂ case explicitly (both modifications are to the same document's vspace, which is consistent).

### Issue 7: vspace subspace structure used but undefined
**ASN-0002, The system state**: "`vspace(d) : Pos → Addr`"
**Problem**: The system state defines vspace as a function from positions to addresses, but AP6 refers to "subspace s of document d," AP10 refers to "text_subspace," and the CREATENEWVERSION section says "The link subspace of the source is not copied." These all assume that Pos has internal structure distinguishing subspaces, but the system state definition does not specify this structure. The reader cannot evaluate AP6 or AP10 without knowing what "subspace" means within the domain of vspace(d).
**Required**: Either (a) define Pos as a structured type (e.g., Pos = Subspace × Nat, or Pos as tumbler addresses with subspace prefixes) so that AP6 and AP10 are well-formed, or (b) introduce the subspace structure explicitly before the properties that rely on it.

## OUT_OF_SCOPE

### Topic 1: Operations not yet covered
**Why defer**: Document creation (as distinct from version creation), account creation, node creation, and administrative operations may exist in the broader system. These would need their own AP-preservation proofs. This is new territory requiring its own operation definitions, not an error in the six operations analyzed here.

### Topic 2: Degenerate operation cases
**Why defer**: Zero-length INSERT, zero-length DELETE, COPY of zero bytes — these are trivially AP-preserving (nothing is allocated or modified) but the operational semantics ASN should specify whether they are legal. Permanence is unaffected.

### Topic 3: Crash recovery and allocation frontier durability
**Why defer**: AP4 (monotonic frontier) requires that the frontier never retreat, including across crashes. The ASN's note that the frontier is recomputed from persistent data is suggestive but not a proof. This is an availability/durability concern, not a correctness error in the permanence axioms.
