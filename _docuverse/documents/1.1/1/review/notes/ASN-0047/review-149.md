# Review of ASN-0047

This pass carries the `review-mode.anti-bloat` classifier. The substantive transition machinery is largely sound on its own terms — the state model, the seven elementary transitions, the J-couplings, and the per-state/composite-boundary partition are coherent. My findings concentrate on prose that does not advance reasoning and on one duplication that forces the reader to reconcile two descriptions of the same mechanism.

## REVISE

### Issue 1: Inheritance/provenance essays around K.α, K.λ, and the supersession tables

**ASN-0047, *Elementary transitions* (K.α) and *Link allocation* (K.λ)**: "is inherited from ASN-0093's K.α directly (only the framing of the home-document predicate differs). We restate the emission cases here for narrative continuity"; and for K.λ, "K.λ is therefore fully inherited from ASN-0093 in signature, precondition, and effect (modulo only the totality reframing of the home-document predicate)."

**Problem**: This is new prose around an inherited definition explaining *where it comes from and how faithfully* rather than advancing the definition's meaning — a defensive justification of provenance. The same "inherited from ASN-0093 directly … the E' = E and R' = R conjuncts are not 'inherited' — they are local additions" disclaimer is repeated in *Elementary transitions* and again verbatim in *Amendments to existing transitions* for both K.α and K.λ. The frame deltas (the `E'=E`, `R'=R` additions) are the only object-level content; the surrounding inheritance accounting is meta-prose that recurs across sections.

**Required**: State the frame once, list the locally-added conjuncts, and drop the repeated "inherited directly / only the framing differs / these are not inherited but local additions" accounting. The same applies to the L14a supersession paragraph in the Properties table ("*superseded by* (replaced by, not implied by) … so the replacement is genuine rather than derivational"), which is an essay justifying a document relationship rather than stating an invariant.

### Issue 2: "Non-determinism of K.μ~ realisations" duplicates "Decomposition of K.μ~"

**ASN-0047, *Decomposition of K.μ~* (the *Non-determinism of K.μ~ realisations* block) vs. the later *Realisation of K.μ~ when the existence condition holds* paragraph**: Both passages partition the realisation space into the full-clearance form (`n'_{s_C} = 0`) and partial-suffix forms (`n'_{s_C} = k₀ − 1`); both state the below-cut value-preservation condition `(A u … : M(d)(u) = M(d)(π⁻¹(u)))`; both explain the relation to pointwise fixity under S5 transclusion; and both close with the convention that unqualified matrix cells read as full-clearance.

**Problem**: This is two paragraphs in the same document saying the same thing in different words. A reader must verify the two statements of the below-cut condition agree (they quantify once over the image `u`, once over the source `v` with a "must range over the image, not the source" caveat appearing in only one place), which is exactly the reconciliation work the anti-bloat lens flags.

**Required**: Merge into a single statement of the realisation family (full-clearance + partial-suffix admissibility condition + pointwise-fixity relation), and cite it once from the matrix-convention note rather than restating it in both blocks.

### Issue 3: Multiple deferrals to the same downstream location

**ASN-0047, *Decomposition of K.μ~* and surrounding sections**: The two-distinct-values precondition's necessity is announced in three places — "Necessity is what we prove" (precondition statement), "Necessity of the two-distinct-values condition is proved in *Decomposition* below" (bulleted deferral), and the actual *Necessity argument* paragraph. Likewise the K.μ⁻ admissible shape defers forward ("see *K.μ⁻ admissible contraction shape* for the equivalence proof") from the K.μ⁻ definition, the matrix cell, and the *PerSubspaceScope* amendment.

**Problem**: Multiple paragraphs in different sections defer to the same downstream location for the same proof. The forward pointer itself carries no content; it is navigational scaffolding that accumulates across cycles.

**Required**: Keep the proof at one site and one forward pointer to it; delete the intermediate "is proved below / see X below" announcements that neither state nor advance the claim.

### Issue 4: Reviser-drift — non-obligation and non-repetition annotations in K.δ

**ASN-0047, *Elementary transitions* (K.δ case (ii))**: The structural-identities catalogue is introduced as "named here for direct citation, *not* repeated as per-sub-case preconditions," and the k=0 rationale notes "The companion structural identities `parent(t) = parent(e)` and `zeros(t) = zeros(e)` … are not separate caller obligations — they appear in the structural-identities catalogue below."

**Problem**: These sentences describe the document's own bookkeeping (what is and is not a precondition, where an identity is catalogued) rather than the operation. They are use-site/non-repetition inventory — a record of editorial intent that a precise reader must skip past to reach the actual precondition list.

**Required**: List the operand-admissibility preconditions for each sub-case and the derived identities (K.δ-ID.*) as facts; remove the meta-commentary stating which of them are *not* obligations and where they are *not* repeated.

### Issue 5: Notation section enumerates downstream consumers

**ASN-0047, *Notation* (Entity-level allocator entry)**: "The content and link sub-allocators `A_C(d), A_L(d)` introduced under SubAllocatorAxiom are *not* entity-level — their outputs inhabit `dom(C) ∪ dom(L)` at zeros = 3."

**Problem**: A notation entry whose body is a contrastive note about which downstream construct is *excluded* from the term is a use-site disambiguation, not a definition of the term being introduced. Similar "introduced here" / "both spellings appear … denotationally identically" annotations elsewhere in the section are housekeeping.

**Required**: Define the entity-level allocator positively (outputs with `zeros ≤ 2`); drop the contrast against `A_C/A_L`, which belongs at — and already appears in — the *Allocator hierarchy under documents* section.

## OUT_OF_SCOPE

### Topic 1: Link-withdrawal mechanism reconciling tombstoning with D-CTG★/D-MIN★
**Why out of scope**: Interior link withdrawal (status flag / tombstone / retraction-link) is correctly identified by the ASN as outside K.μ⁻'s presentational-removal contract and deferred to future work in Open Questions. The current ASN's suffix-only contraction is internally consistent; the richer mechanism is new territory, not an error here.

### Topic 2: Abstract specification of the external node-allocation registry
**Why out of scope**: NodeUniqueAllocation and NodeRegistryBootstrap rest on an external registry; whether its issuing protocol/persistence/concurrency should be specified abstractly is genuinely a future-ASN boundary question, already catalogued in Open Questions. The axioms suffice as the docuverse-layer abstraction boundary for this ASN.

VERDICT: REVISE
