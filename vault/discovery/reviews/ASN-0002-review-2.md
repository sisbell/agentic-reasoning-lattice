# Review of ASN-0002

## REVISE

### Issue 1: AP5 is false as stated; link survivability derivation is unsound
**ASN-0002, AP5 and "Link survivability as consequence"**: "Editing operations modify V-space; they do not modify I-space."
**Problem**: INSERT extends `dom.ispace` with fresh addresses and writes content there. CREATELINK extends `dom.ispace` with a fresh link address. Both operations modify I-space. AP5 as stated is false for two of the six operations the ASN defines. The link survivability derivation cites AP5 as premise 3: "Editing operations modify only V-space (AP5, AP7, AP8)." The word "only" is false for INSERT and CREATELINK, so the derivation chain is broken.
**Required**: AP5 must distinguish between mutating existing I-space entries (forbidden) and monotonically extending I-space (permitted). A precise statement: "Editing operations do not modify or remove existing entries in I-space; they may only extend `dom.ispace` with fresh addresses." The link survivability derivation must then cite this corrected form and show that monotonic extension of I-space does not affect existing link endset references — which it does not, but the argument must use the correct premise.

### Issue 2: System state Σ omits `links`; AP12 quantifies over an undefined set
**ASN-0002, "The system state" and AP12**: Σ is defined as containing `ispace`, `vspace(d)`, and `spanindex`. AP12 quantifies over `(A link ∈ links, e ∈ endsets(link) : ...)`.
**Problem**: The set `links` and the function `endsets` are never defined as components of Σ or derived from its components. CREATELINK's analysis implies that links are stored in `ispace` (it "extends `dom.ispace` with a fresh address in the link subspace"), but this is stated only in the operation analysis, not in the system state definition. AP12 quantifies over a set that has no formal standing.
**Required**: Either (a) add `links` and their structure to Σ's definition and explain the relationship to `ispace`, or (b) define `links` as a derived set from `ispace` (the subset of `dom.ispace` in the link subspace) and show AP12 follows from AP1.

### Issue 3: AP12 is derivable from AP1 but presented as independent
**ASN-0002, AP12**: "A link's endset I-addresses are not affected by any editing operation" — introduced as a new property.
**Problem**: If links are stored in `ispace` (as CREATELINK's analysis states), then a link at address `ℓ` has content `ispace.ℓ` which includes its endset I-addresses. AP1 guarantees `ispace'.ℓ = ispace.ℓ`, so the endset addresses cannot change. AP12 is a corollary of AP1, not an independent axiom. Presenting it as "introduced" obscures the logical structure and inflates the property count without adding strength.
**Required**: Derive AP12 from AP1 explicitly. State the premises: (1) links are stored in `ispace`, (2) endset I-addresses are part of the content at the link's I-address, (3) AP1 guarantees that content is immutable. Conclusion: endset I-addresses are immutable. Label AP12 as "derived" in the properties table.

### Issue 4: `vspace(d)` typed as total function but used as partial
**ASN-0002, "The system state"**: `vspace(d) : Pos → Addr`
**Problem**: A total function from `Pos = Subspace × Nat` to `Addr` has infinite domain. But the ASN uses `#vspace(d)` for the "length" of document d's virtual stream, implying a finite domain. DELETE "removes entries" from `vspace(d)` — you cannot remove entries from a total function. INSERT "creates new V-positions" — in a total function, every position already exists.
**Required**: Type `vspace(d)` as a partial function `vspace(d) : Pos ⇀ Addr` (matching the `⇀` notation used for `ispace`), or define it as a total function on a finite domain `{0, ..., #vspace(d)-1}` that changes with operations. The operations' effects on vspace must be consistent with the chosen type.

### Issue 5: AP8 formalizes only one direction; the bijectivity claim is half-proved
**ASN-0002, AP8**: `(A a : (E p : vspace(d).p = a) : (E p' : vspace'(d).p' = a))`
**Problem**: The prose says "The set of I-addresses referenced by the document is unchanged — only the mapping from V-positions to those I-addresses changes." Set equality requires two directions: every old address survives (stated) AND no new address appears (not stated). AP8 formalizes only the first direction. The reverse — `(A a : (E p' : vspace'(d).p' = a) : (E p : vspace(d).p = a))` — is missing. Without it, AP8 permits REARRANGE to silently introduce new I-address references, contradicting the "unchanged" claim.
**Required**: State AP8 as a set equality: `{a : (E p : vspace(d).p = a)} = {a : (E p' : vspace'(d).p' = a)}`. Or state both directions explicitly. The proof should show that REARRANGE permutes V-positions without altering the codomain.

### Issue 6: AP14 is ambiguous for multi-document operations
**ASN-0002, AP14**: "No operation on document d₁ modifies the V-space mapping of document d₂ ≠ d₁"
**Problem**: COPY takes a source document `d₁` and a target document `d₂`, modifying `vspace(d₂)`. Is COPY "on" `d₁` or `d₂`? If COPY is "on d₁," AP14 is violated (it modifies `d₂ ≠ d₁`). If COPY is "on d₂," AP14 holds. Similarly, CREATENEWVERSION creates a new document `d'` from source `d` — is it "on d" or "on d'"? The phrase "operation on document d₁" is undefined, making AP14 unverifiable.
**Required**: Define what it means for an operation to be "on" a document. One approach: each operation has a *target document* (the one whose V-space it modifies), and AP14 asserts that only the target document's V-space is modified. State this precisely and verify for each operation, including COPY (target is `d₂`; source `d₁` is read-only) and CREATENEWVERSION (target is the new `d'`; source `d` is read-only).

### Issue 7: No concrete worked example
**ASN-0002, throughout**: The ASN cites Gregory's empirical evidence in several places (e.g., addresses `α₁, α₂, α₃` for "ABC") but never works through a complete scenario checking the postconditions systematically.
**Problem**: The review standard requires at least one concrete scenario verifying key postconditions. The ASN has none. A reader cannot check AP0, AP1, AP2, and the frame conditions against a specific sequence of operations.
**Required**: Work through one scenario — e.g., INSERT "AB" into an empty document (allocating `α₁, α₂`), then DELETE the first character, then COPY the surviving character to a new document, then CREATELINK referencing `α₁`. At each step, verify: (1) `dom.ispace` only grows, (2) `ispace.α₁` and `ispace.α₂` are unchanged, (3) `α₁` remains in `dom.ispace` after DELETE though it's no longer in `vspace(d)`, (4) the link's endset still references valid I-addresses. This grounds the abstract argument.

### Issue 8: Ghost address permanence is asserted but not derived
**ASN-0002, "Ghost addresses"**: "A ghost address is not available for reuse. It is a permanent commitment to a position in the address space, even without associated content."
**Problem**: AP0 protects addresses in `dom.ispace`. Ghost addresses are explicitly NOT in `dom.ispace`. AP4 (monotonic frontier) prevents new *allocations* from landing on ghost addresses below the frontier, but "not available for reuse" is a broader claim than "no allocation will land here." What prevents a ghost address from being reassigned to a different entity (e.g., a different document or user)? The ASN says "we need not formalize ghost elements" and then relies on their permanence in the link survivability argument ("links may be made to them"). Informal permanence for a formally-used concept is a gap.
**Required**: Either formalize ghost address permanence (e.g., introduce a property that the assignment of address-space ranges to nodes/users/documents is monotonic and irrevocable) or weaken the claims to what AP4 actually establishes: "no content allocation will fill a gap below the frontier." If links to ghost addresses are architecturally important, the permanence of those addresses needs a formal basis.

### Issue 9: CREATENEWVERSION — "does not enter `dom.ispace`" is asserted without formal grounding
**ASN-0002, CREATENEWVERSION section**: "This address does not enter `dom.ispace`. It is a ghost address... The document identity is recorded in the system's document registry (a component of Σ outside ispace)."
**Problem**: The "document registry" is not defined in Σ. The claim that the document identity address does not enter `dom.ispace` is backed only by implementation evidence ("No content allocation function is invoked"). At the specification level, what constrains CREATENEWVERSION from allocating a content address for the document identity? The main theorem's proof for CREATENEWVERSION relies on this claim ("does not enter `dom.ispace`"), making it load-bearing.
**Required**: Either (a) add the document registry to Σ and specify that CREATENEWVERSION writes to the registry, not to `ispace`, or (b) state as a precondition/effect of CREATENEWVERSION that it allocates no content addresses, justified by the specification of what a "document identity" is (an address-space position, not a content entry). The distinction between content addresses and identity addresses needs formal standing.

## DEFER

### Topic 1: Atomicity and concurrency model
**Why defer**: The ASN implicitly assumes sequential execution of operations. Concurrent operations (e.g., two simultaneous INSERTs into the same document) raise questions about freshness (AP2) and V-space consistency that require a separate treatment. This ASN correctly establishes the sequential invariants that a concurrency model must preserve.

### Topic 2: Zero-width and empty-endset edge cases
**Why defer**: The ASN does not address INSERT of zero bytes, COPY of zero bytes, REARRANGE of a zero-width region, or CREATELINK with empty endsets. These are boundary conditions that should be specified (are they no-ops? are they precondition violations?) but they do not threaten the core permanence argument — they are specification completeness issues for the individual operations.

### Topic 3: Spanindex maintenance obligation
**Why defer**: The ASN explicitly defers this: "which operations must write spanindex entries and when — is deferred." The forward correspondence property (every live V-space reference is indexed) requires per-operation verification that is cleanly separable from the permanence argument.

### Topic 4: Allocation frontier crash recovery
**Why defer**: The ASN notes that the allocation counter is "recomputed from the content store on each allocation" but does not analyze crash scenarios. Recovery guarantees are a system-level concern beyond the scope of address permanence as an abstract property.
