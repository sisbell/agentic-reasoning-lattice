# Review of ASN-0002

## REVISE

### Issue 1: AP5 is formally identical to AP
**ASN-0002, The two-space architecture**: "AP5 (Dual-space contract). Editing operations do not modify or remove existing entries in I-space. They may only extend dom.ispace with fresh addresses: `(A a : a ∈ dom.ispace : ispace'.a = ispace.a) ∧ dom.ispace ⊆ dom.ispace'`"
**Problem**: The formula is `AP1 ∧ AP0` — identical to AP. The prose promises more ("with fresh addresses") but the formula doesn't capture freshness. AP already quantifies over *every* operation, so AP5 adds nothing. The properties table labels AP5 "derived" but names no premises and gives no derivation chain — the derivation is the entire main theorem, making the relationship circular (AP5 summarizes the theorem that proves AP, which equals AP5).
**Required**: Either (a) strengthen the formula to include AP2 — `... ∧ (A a : a ∈ dom.ispace' \ dom.ispace : a was fresh per AP2)` — making AP5 genuinely stronger than AP, or (b) relabel AP5 as a restatement of AP specialized to the dual-space context, not a derived property.

### Issue 2: AP4 implies AP2 only with an unstated premise
**ASN-0002, The freshness obligation**: "AP4 implies AP2 (fresh addresses are above all existing ones, hence disjoint from them) but is strictly stronger"
**Problem**: AP4 guarantees monotonic frontier *within each partition*. AP2 requires freshness across *all* of `dom.ispace`. The implication holds only if partitions have structurally disjoint address ranges — a property stated in prose ("text addresses begin with subspace identifier 1, link addresses with identifier 2") but never formalized. Without it, an address above the text-subspace frontier could still collide with a link-subspace address.
**Required**: State partition disjointness as a formal property — e.g., `text_subspace ∩ link_subspace = ∅` at the address-range level — and cite it explicitly in the AP4 ⟹ AP2 chain.

### Issue 3: Boundary cases absent from operation analysis
**ASN-0002, Operation-by-operation analysis**: All six operations analyzed for the typical case only.
**Problem**: No operation is analyzed at zero width. INSERT of empty string — are zero addresses allocated? AP2 is vacuously satisfied, but the ASN doesn't state this. DELETE of empty range — is it a no-op? COPY of zero characters — does the target document gain zero V-positions? CREATELINK with an empty endset — is a link with no span descriptors valid? The structural arguments handle degenerate inputs implicitly (the proofs don't break), but the ASN never acknowledges the boundary or confirms the behavior.
**Required**: For each operation, state explicitly what happens at zero width. One sentence per operation suffices: "INSERT of zero characters allocates no addresses and is a no-op on both I-space and V-space." Likewise for CREATELINK with empty endsets — state whether this is a valid operation or a precondition violation.

### Issue 4: REARRANGE precondition proposed but not adopted
**ASN-0002, REARRANGE**: "The abstract precondition should include: `(A p : p ∈ dom.vspace(d) ∧ p is affected by REARRANGE : subspace(p') = subspace(p))` ... We note this as a required precondition that the implementation does not enforce."
**Problem**: The ASN identifies a subspace-boundary violation, calls the guard "required," and then does not include it in REARRANGE's specification. A future ASN building on this one would find REARRANGE specified without the guard and would be entitled to assume cross-subspace rearrangement is permitted. The ASN contradicts itself: the precondition is simultaneously "required" and absent.
**Required**: Either (a) adopt the precondition formally into REARRANGE's specification (add it alongside the cut-point constraints), or (b) weaken the language from "required precondition" to "recommended guard for a future ASN on V-space discipline" and state explicitly that this ASN's REARRANGE permits cross-subspace displacement.

### Issue 5: CREATENEWVERSION proof depends on an undefined Content type
**ASN-0002, Theorem proof, CREATENEWVERSION case**: "The document identity address is not a content address and does not enter `dom.ispace`"
**Problem**: The state model defines `ispace : Addr ⇀ Content` but never defines `Content`. The CREATENEWVERSION proof asserts that a POOM orgl (the document's structural mapping node) is not a `Content` value — this is the critical step that prevents the document identity address from entering `dom.ispace`. But without a definition of `Content`, the distinction between "content stored at an address" and "structural metadata at an address" has no formal basis. The proof step is an informal claim inside a formal proof.
**Required**: Define `Content` in the state model section — at minimum, state that `Content = TextContent | LinkStructure` (or whatever the intended sum type is) and that structural metadata (POOM orgls, allocation tree nodes) are not values of type `Content`. This gives the CREATENEWVERSION proof case a formal hook.

### Issue 6: AP10 missing postcondition for new version's link subspace
**ASN-0002, CREATENEWVERSION**: "The link subspace of the source is not copied — the new version begins with text content only."
**Problem**: AP10 formalizes the text-subspace equality between source and new version. The frame condition says the link subspace is not copied. But there is no formal postcondition stating that the new version's link subspace is empty: `{p ∈ dom.vspace'(d') : p.subspace = link_subspace} = ∅`. This is implied by "text content only" but unstated. A future ASN reasoning about the new version's link subspace has no formal property to cite.
**Required**: Add a formal postcondition to CREATENEWVERSION: the new version's V-space contains no link-subspace entries.

## OUT_OF_SCOPE

### Topic 1: Content type full formalization
**Why out of scope**: A complete definition of the `Content` type — its constructors, equality semantics, and relationship to structural metadata — is a foundational concern that belongs in a state-model ASN. This ASN needs only a minimal definition (Issue 5) to close the CREATENEWVERSION gap.

### Topic 2: Spanindex maintenance obligation
**Why out of scope**: The ASN explicitly defers verification of the forward direction `(A d, a : (E p : vspace(d).p = a) ⟹ (a, d) ∈ spanindex)`. This requires specifying, for each V-space-creating operation, that it also writes spanindex records. A future ASN on index maintenance.

### Topic 3: Link discovery mechanism
**Why out of scope**: The ASN correctly notes that AP13 establishes endset *validity* but not *discoverability*. A mechanism mapping content I-addresses to links is needed but is a distinct indexing problem, not an address permanence property.

### Topic 4: CREATELINK V→I resolution for non-contiguous results
**Why out of scope**: When a contiguous V-range maps to non-contiguous I-addresses (e.g., after REARRANGE), the V→I lookup produces multiple spans. The packaging algorithm — how the system segments non-contiguous I-addresses into span descriptors — is an operation-specification detail that belongs in a CREATELINK-focused ASN, not here.

VERDICT: REVISE
