# Review of ASN-0047

This is a substantial and largely rigorous ASN. The elementary-transition taxonomy, the two-subspace generalization (S3★, D-CTG★/D-MIN★/D-SEQ★), the K.μ~ fixity argument, and the per-state vs. composite-boundary invariant split are carefully constructed, and I found no correctness defect in the core proofs (FrontierEquivalence, K.μ~ subspace preservation, the necessity/sufficiency precondition, GlobalLineage all check out). The findings below are prose-quality and one structural-clarity issue — the document carries the `review-mode.anti-bloat` classifier, and there is accumulated meta-prose to flag.

## REVISE

### Issue 1: Vestigial `J1`/`J1'` and the first `ValidComposite` definition are superseded before they are ever used
**ASN-0047, *Coupling and isolation* / *Scoped coupling constraints***: The early "Definition (Valid composite transition)" stipulates "(2) Coupling constraints: J0, J1, and J1' hold for the composite." But J1 and J1' are introduced only as redirect stubs — "The operative coupling is J1★ ... over the link-free fragment ... J1★ reads ..." — and the subsequent ValidComposite★ supersedes the whole definition by "replacing J1/J1' with J1★/J1'★."
**Problem**: The reader is handed a Definition and two coupling constraints that are obsolete at the moment of introduction. The state model is `Σ = (C, L, E, M, R)` from the outset, so the "link-free fragment" is a special case, not a separate model; J1/J1' and the first ValidComposite advance no reasoning that J1★/J1'★/ValidComposite★ don't carry. This is the "two paragraphs say the same thing" pattern, compounded by indirection (J1 *is* J1★ "operatively").
**Required**: Either define only J1★/J1'★/ValidComposite★ and drop J1/J1' and the first ValidComposite, or demote the link-free forms to a single inline sentence ("in states with no link subspace these reduce to the unscoped J1/J1'") rather than standalone definitions that get retracted.

### Issue 2: Cross-ASN lineage narration in the property tables
**ASN-0047, *Inherited from foundation* and *Local extensions* tables**: e.g. L1c — "Originated in ASN-0093 as the structural-inc-chain form (weakened from ASN-0043's 'operates within a system conforming to T10a') ... ASN-0047 inherits this form unchanged"; L14 — "SD's unscoped form already supersedes ASN-0043's scoped L14 (DualPrimitive ...), the unscoping being available because ASN-0093's K.α `E(a)₁ = s_C` precondition forces every `a ∈ dom(C)` to be `s_C`-resident."
**Problem**: These cells narrate the genealogy of a definition across three ASNs rather than stating the property and its source. The provenance ("weakened from X's phrasing," "already supersedes Y's scoped form") belongs in a changelog, not in a property-statement slot; it is exactly the cross-cycle accretion the anti-bloat classifier targets, and a reader must skip it to reach the operative statement.
**Required**: Reduce each cell to the property and a single foundation citation. Drop the inter-ASN "weakened from / supersedes / unscoping available because" lineage prose.

### Issue 3: Definition entries enumerate their downstream consumers
**ASN-0047, *Properties Introduced* table**: TrackedEmission — "Supplies the *existence* of the owning allocator A that FrontierEquivalence then resolves to uniqueness via T10a.6"; FrontierEquivalence's entry similarly forward-points to its own consumers.
**Problem**: A definition's table entry should advance the definition's meaning, not inventory which later lemma consumes it. "Supplies the existence that X then resolves" is a use-site note, not content.
**Required**: State what TrackedEmission asserts (every non-node entity inhabits a tracked sub-allocator domain) and stop. Move the "feeds FrontierEquivalence" relationship, if needed at all, to FrontierEquivalence's own proof where it is used.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: The ASN deliberately starts a forked document's link subspace empty and routes discovery through shared I-addresses; a mechanism for copying source links is new operational territory, already flagged in Open Questions, not an error here.

### Topic 2: Interior link withdrawal / tombstoning
**Why out of scope**: K.μ⁻ admits only per-subspace suffix truncation under D-CTG★/D-MIN★, so withdrawing an interior link requires a separate mechanism. The ASN correctly confines this to Open Questions rather than under-specifying K.μ⁻.

VERDICT: REVISE
