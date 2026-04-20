# Review of ASN-0002

## REVISE

### Issue 1: CREATELINK's V-space effect is unspecified
**ASN-0002, CREATELINK section**: "Effect on ispace. CREATELINK extends dom.ispace with a fresh address in the link subspace."
**Problem**: The state definition establishes that V-space positions are structured as `Pos = Subspace × Nat`, with a link subspace holding link addresses. The vocabulary confirms documents have two subspaces: text content (1.x) and links (0.x). Yet the CREATELINK section specifies only the I-space effect. The frame conditions say "does not modify any document's text subspace mapping" — conspicuously silent about the link subspace. If CREATELINK adds a V-position in the target document's link subspace (as the state model implies it must), this effect is missing. If CREATELINK does NOT modify any V-space, then links have I-space presence but no V-space presence, and the link subspace of V-space is never populated by any of the six operations — making it a dead component of the model. The worked example (Step 4) compounds the gap: it creates a link without specifying which document hosts it.
**Required**: State CREATELINK's V-space effect explicitly. Either it inserts a V-position in the target document's link subspace (and state the target, the shift behavior, and the subspace isolation guarantee), or it does not modify any V-space (and explain how links are associated with documents without V-space presence).

### Issue 2: Endset reference domain contradicts ghost address linkability
**ASN-0002, The system state**: "A link structure at address ℓ contains endset I-addresses — references to other addresses in dom.ispace."
**ASN-0002, Ghost addresses**: "these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them."
**Problem**: The state definition constrains endset references to addresses in `dom.ispace`. Ghost addresses are explicitly stated to be NOT in `dom.ispace` — they are structural positions without stored content. Yet the ghost address section states links can reference them. These two claims are inconsistent. Either endset references can include addresses outside `dom.ispace` (weakening the state definition), or links to ghost elements work through a different mechanism than endset I-address references (which must be explained). The inconsistency also affects CREATELINK's precondition, which is never stated: must endset references be in `dom.ispace` at creation time?
**Required**: Resolve the contradiction. If endsets are spans (start + length, per the vocabulary), clarify that the stored span description may cover addresses not in `dom.ispace`, and distinguish the immutable span from the set of content addresses it currently covers. If endsets can only reference `dom.ispace` members, retract the ghost address linkability claim or explain the alternative mechanism.

### Issue 3: AP4a is stated about structure not present in Σ
**ASN-0002, Ghost addresses**: "AP4a (Range commitment permanence). ... entity(r)' = entity(r) for every operation."
**Problem**: The system state Σ contains `ispace`, `vspace(d)`, and `spanindex`. The function `entity : Range → Entity` that maps address ranges to servers, accounts, or documents is not part of Σ. AP4a uses primed-state notation as if it were a formal state invariant, but it quantifies over a function that the model does not define. The property is formally vacuous — it cannot be verified against the model because the model doesn't contain the structure it references. The CREATENEWVERSION section acknowledges that document identity lives in "the global allocation tree" rather than `ispace`, but this tree is also absent from Σ.
**Required**: Either extend Σ to include the range-to-entity mapping (so AP4a becomes a verifiable state invariant), or demote AP4a to a design-level requirement stated informally, without the formal `entity(r)' = entity(r)` notation that implies it is grounded in the model.

### Issue 4: REARRANGE's precondition is absent
**ASN-0002, REARRANGE section**: "REARRANGE transposes regions within a document's virtual stream."
**Problem**: No precondition is stated. What are the "regions"? Two disjoint contiguous ranges? Possibly overlapping? Possibly empty? The claim that REARRANGE is a "pure permutation" (AP8) depends on what inputs are valid. If regions overlap, the operation is not a permutation. If one region is empty, AP8 holds trivially but the operation's V-space effect needs different case analysis. If a region extends beyond `dom.vspace(d)`, the operation is undefined. Without a precondition, AP8 cannot be verified at boundaries — it is a claim about an operation whose valid inputs are unspecified.
**Required**: State REARRANGE's precondition: what arguments it takes, what constraints they must satisfy (disjoint? contiguous? non-empty? within bounds?), and verify AP8 holds under that precondition.

### Issue 5: Five derived properties are labeled "introduced" in the properties table
**ASN-0002, Properties Introduced table**:
- **AP3**: Table says "introduced," text says "follows from AP0 ∧ AP2." Should be "derived."
- **AP5**: Table says "introduced," but AP5 is AP0 ∧ AP1 restricted to editing operations — follows from properties already stated for all operations. Should be "derived."
- **AP13**: Table says "introduced," but it follows from AP0 (address persists) + AP1 (content unchanged) + AP9 (COPY shares I-addresses). Should be "derived."
- **AP15**: Table says "introduced," text says "This follows from AP14 ... and AP0." Should be "derived."
- **AP7**: Table says "introduced," but AP7 (`dom.ispace' = dom.ispace ∧ ispace'.a = ispace.a`) is a specialization of AP for DELETE. Should be "derived."

**Problem**: The introduced/derived distinction matters for dependency tracking. A property labeled "introduced" is an axiom — it must be independently justified. A property labeled "derived" depends on earlier properties — its justification is the derivation chain. Mislabeling derived properties as introduced obscures the dependency structure and could lead future ASNs to treat corollaries as independent axioms.
**Required**: Correct the labels: AP3, AP5, AP7, AP13, AP15 → "derived."

## OUT_OF_SCOPE

### Topic 1: Link discovery mechanism
**Why out of scope**: The ASN explicitly notes that "A link-discovery mechanism ... is needed but is not defined in this ASN." This is a separate functional requirement (indexing infrastructure), not a permanence property. AP12 establishes that link references survive; how to find them is a different question.

### Topic 2: Spanindex maintenance obligation
**Why out of scope**: The ASN explicitly defers: "We do not verify this invariant here." The forward direction (`vspace(d).p = a ⟹ (a,d) ∈ spanindex`) requires per-operation verification of spanindex writes. AP11 establishes the monotonicity envelope; the maintenance obligation is new specification work.

### Topic 3: V-space operational completeness
**Why out of scope**: The ASN underspecifies V-space effects beyond ispace permanence — COPY's shift behavior in the target, INSERT and DELETE at boundary positions (position 0, last position, empty document), and whether `dom.vspace(d)` is always contiguous. These are important for a V-space operations ASN but are not errors in the permanence analysis, which is correctly scoped to ispace invariants.

VERDICT: REVISE
