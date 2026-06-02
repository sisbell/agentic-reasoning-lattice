# Review of ASN-0047

This is the transition-model ASN carrying the `review-mode.anti-bloat` classifier. The core argument — five-component state, seven elementary transitions, the per-state/composite-boundary invariant split, and the destruction-confinement theorem — is sound and the worked examples are genuinely load-bearing (order/multiplicity preservation, depth rebasing, duplicate-source, prior-vs-first-time provenance). I am not flagging the worked examples or overall length (per the standing scope and the declined sprawl findings). The findings below target meta-prose accretion and two precision defects.

## REVISE

### Issue 1: The K.μ~ shape-invariant discharge is a cross-section deferral loop with duplicated derivation
**ASN-0047, K.μ~ definition (admissibility clause (i)) and Class (a) proof paragraph "K.μ~ discharge for the arrangement-shape invariants"**: Clause (i) reads "...the derived D-SEQ★ follows (D-CTG★ + D-MIN★ + S8-depth + S8a, together with S8-fin(Σ') — the latter not part of the shape package but supplied independently by the operational *K.μ~ discharge for the arrangement-shape invariants*)", which forward-points into the Class (a) proof; that proof paragraph then re-derives the same thing ("S8-fin(Σ') ... is discharged independently ... K.μ⁻ restricts ... K.μ⁺ adds ... D-SEQ★ is then derived ... via the standard D-SEQ★ derivation"). The same S8★ obligation is also deferred twice ("by Step (B)" for S3★, and "by the inherited K.μ⁺ and K.μ⁻ S8★ columns (the ... matrix entry in *Extended reachable-state invariants*)").
**Problem**: This is the "multiple paragraphs defer to the same downstream location" + "two paragraphs say the same thing in different words" pattern. A reader following clause (i) is bounced to a named paragraph that bounces back. The S8-fin/D-SEQ★ derivation is stated in both places.
**Required**: Pick one site. State the S8-fin(Σ') and derived-D-SEQ★ discharge once (the Class (a) paragraph is the natural home) and have clause (i) name it without restating the derivation, or inline it into clause (i) and delete the standalone paragraph's restatement.

### Issue 2: ValidComposite★ lists the named composite K.μ~ as an atomic transition
**ASN-0047, ValidComposite★**: "a finite sequence of *atomic* transitions `Σ = Σ₀ → ... → Σₙ = Σ'` — drawn from K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, and K.ρ".
**Problem**: K.μ~ is defined throughout as a *named composite* (K.μ⁻ + K.μ⁺), not an atomic transition, so its inclusion in "a finite sequence of atomic transitions" is a self-contradiction that the reader must reconcile against the later parenthetical "K.μ~ appearing in the sequence is shorthand for its K.μ⁻ + K.μ⁺ decomposition." The "drawn from" set conflates the atomic vocabulary with one composite.
**Required**: List only the eight atomic transitions in the "atomic sequence" clause and state separately that K.μ~ may appear as shorthand expanding to its two-step decomposition — rather than seating the composite inside the atomic enumeration.

### Issue 3: S4 verification paragraph carries defensive "what it is NOT" prose plus a use-site inventory
**ASN-0047, Class (a), S4 paragraph**: "The related allocator-discipline distinctness obligations for entities (K.δ) and link addresses (K.λ) are *not* S4 obligations — S4 is content-only — and are carried by the *Entity distinctness* and *L11a* matrix rows above."
**Problem**: This is meta-prose: it explains what S4 does not cover and inventories which other matrix rows carry the related obligations, rather than advancing S4's own content-store discharge. The matrix already has distinct rows for Entity distinctness and L11a; the cross-pointer is navigational noise.
**Required**: Drop the "not S4 / carried by rows X and Y" sentence; the S4 paragraph need only state the K.α freshness + CrossDocDisjoint discharge over `dom(C)`. The separation from entity/link distinctness is already visible from the separate matrix rows.

### Issue 4: SubAllocatorBundle opens with an inherited-facts inventory
**ASN-0047, "Sub-allocator activation (SubAllocatorBundle)"**: "The standing properties of these chains — [T10a-conforming discipline; determinate first emission; T4-validity] — are all foundation facts (ChainDiscipline, ChainEnumerationInjectivity, FirstEmission, FirstEmissionFreshness, ChainElementT4Validity, DisjointSubAllocatorChains, all ASN-0093). The one obligation the bundle must discharge beyond these foundation facts is the cross-subspace disjointness delta."
**Problem**: The six-lemma parenthetical is an inherited-fact inventory whose only working content is the final clause isolating the delta. The catalog restates that the chain properties come from ASN-0093 — which the per-property prose and the *Inherited from foundation* table already establish.
**Required**: Compress to the load-bearing statement (the bundle inherits the chain properties from ASN-0093 and must discharge only the cross-subspace disjointness delta) without re-enumerating the named lemmas; cite the specific lemma only where the delta proof consumes it (CrossDocDisjoint, DisjointSubAllocatorChains).

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement contraction with renumbering (DELETEVSPAN compaction)
**Why out of scope**: The ASN's K.μ⁻ models suffix removal only; interior compaction-and-renumber is named operation mechanics, already deferred to an Open Question, and DELETEVSPAN is in the declared scope exclusions.

### Topic 2: Concurrency / serialization of allocation under a shared home document
**Why out of scope**: SequentialTransitionAxiom fixes a totally-ordered atomic model; concurrent allocation is new territory, correctly held as an Open Question rather than an error here.

### Topic 3: Transitive transclusion-chain provenance and endset-participation permanence
**Why out of scope**: These are genuinely future invariants over R and link endsets; the ASN appropriately lists them as Open Questions and does not under-specify them in the current model.

VERDICT: REVISE
