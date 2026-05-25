# Review of ASN-0094

## REVISE

### Issue 1: Cross-ASN references to non-foundation ASNs (ASN-0036, ASN-0093)
**ASN-0094, Definition — SubstrateConformingLayer**: "The full L/S/M/C invariant list of ASN-0036, ASN-0043, and ASN-0093: ... *ASN-0036 content/arrangement invariants:* S0, S1, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ. *ASN-0093 substrate invariants:* M0, M1, C0, C1, C1b, C1c, C-fin."
**Problem**: Foundation ASNs are ASN-0034, ASN-0043, ASN-0086. References to ASN-0036 and ASN-0093 (and named claims from them: ChainMembershipForOrigin, DisjointSubAllocatorChains, CrossDocDisjointness, etc.) appear throughout without those ASNs being declared foundation. The same pattern recurs in citations of L0a (ContentSubspaceScope from ASN-0043 — OK) alongside undeclared invariants.
**Required**: Either declare ASN-0036 and ASN-0093 as additional foundation ASNs, or restrict the ASN to citing foundation invariants and locally stated scaffolding clauses only.

### Issue 2: Redundant restatement of ASN-0086's SubstrateConformingLayer
**ASN-0094, Definition — SubstrateConformingLayer**: The entire definition (catalogs (a) and (b)) duplicates ASN-0086's foundation definition verbatim, with the same invariant-catalog references.
**Problem**: The restatement contributes nothing the foundation definition doesn't already supply, but it imports non-foundation references into ASN-0094's text. The scaffolding clauses listed later (*Substrate-conforming-layer scaffolding*) are what the framework's proofs actually cite by name; the broader definition is dead weight.
**Required**: Cite ASN-0086's definition by reference and remove the verbatim restatement, OR rely solely on the locally-stated scaffolding clauses and drop the SubstrateConformingLayer definition entirely.

### Issue 3: Meta-prose accretion across multiple sections
**Patterns observed throughout**: Many paragraphs explain framework choices rather than advance the framework's claims. Specific instances:
- "*Per-class consistency of per-K discipline registration*" (Canonical Shape Catalog) — defensive explanation of why registrations must apply at class level.
- "*Catalog row structure: base, opt-in, parametric*" (Canonical Shape Catalog) — meta-organizational explanation of the categorization scheme itself.
- "*Per-K opt-in registry is partitioned by base shape*" — explains the partitioning without advancing content.
- "*Naming convention for framework commitments*" + "*Consolidated commitment reference table*" + "*Contract status and failure modes (framework-level)*" — three consecutive organizational paragraphs in Scope and Substrate Scaffolding.
- "*Without SingleHomeCoverageDiscipline*" (NonIdempotentDirectedPair) — explains what's outside the framework.
- "*Why single-home matters for `emission_order`*" + "*Why the `argmax` in `latest_K_for_addr` is well-defined under T1*" + "*Subset preservation when `d_K` hosts multiple relations*" — three defensive sub-paragraphs in SHCD section.
- "*Layer composite: `K_is_fresh`*" (FDD section) — explicitly notes the composite is "not a Sh5(b)-admissible base template" then includes it anyway.
- "*Scope of the per-tuple-conformance relaxation*" + "*Per-walkthrough convention*" — both elaborate the same baseline assumption already stated.
**Problem**: This is the *new prose around an axiom explains why* and *paragraph looks like a prior finding's content relocated rather than removed* pattern from the anti-bloat classifier.
**Required**: Cut paragraphs that explain choices rather than advance claims. Where motivation is essential, fold it into the affected definition/lemma in one sentence.

### Issue 4: Forward-reference accretion
**Patterns**: Multiple paragraphs defer to downstream locations:
- "see the SingleHomeCoverageDiscipline sub-section below for the discipline's definition, layer-discipline contract, preservation theorem, status, failure modes, and the well-definedness arguments"
- "see the *Asymmetry of `to_K`* note in the walkthrough body for the formal reading"
- "see the framework-level *Contract status and failure modes* paragraph in Scope and Substrate Scaffolding" (appears in three separate per-K discipline sections)
- Catalog rows defer template bodies to walkthroughs: "(bodies in the walkthrough)" for Retraction, BundledDirectedPair, Provenance.
**Problem**: Three discipline sections each defer to the same "framework-level paragraph"; catalog rows defer template bodies to walkthroughs; the walkthroughs back-reference the catalog. The reader cannot pick up cold.
**Required**: Either inline the deferred content at first use, or remove the back-references and let the structure be flat.

### Issue 5: Sh5 is META; the canonical catalog occupies disproportionate space
**ASN-0094, Sh5 — TemplateCatalog (META)**: "Sh5 is an organizational convenience for hand-curating the canonical shape catalog; it is not a mechanical-derivation theorem. ... The framework's actual content is therefore Sh-conf + Sh0–Sh4 + the layer-discipline contracts; the catalog and template families are an organizational layer on top."
**Problem**: The catalog table, eight per-shape walkthroughs, and seven "Additional Worked Examples" together comprise roughly half the document, but Sh5 itself acknowledges these are organizational rather than load-bearing. The hand-curated templates contribute no theorems beyond those Sh0–Sh4 already establish.
**Required**: Move catalog entries and walkthroughs to a separate appendix/companion note, or restrict the catalog section to a single concrete instantiation that exercises every framework primitive once.

### Issue 6: Property table reports types without further classification
**ASN-0094, Properties Introduced**: 36 entries, all marked "introduced" with no derivation chain.
**Problem**: Definitions, lemmas, axioms, and assumptions are mixed in one column. A reader cannot quickly see which entries are load-bearing and which are organizational.
**Required**: Separate the table into "load-bearing claims" (Sh-conf, Sh0–Sh4, the three contracts, the four lemmas/corollaries) and "supporting definitions" (the various symbol introductions).

### Issue 7: Lemma — LinkAddressNotPrefixOfEmit could use the simpler freshness route
**ASN-0094, Lemma — LinkAddressNotPrefixOfEmit Case II.A**: "By T3 (CanonicalRepresentation, ASN-0034) applied to the equal-length componentwise agreement, `b = a`. ... K.λ's construction gives `home(a) = d` in both emission branches. ... Hence `home(b) = d`, contradicting `home(b) ≠ d`."
**Problem**: The case derives `b = a_emit(Σ, d)` then argues by home identity. But ASN-0086's K.λ postcondition `a ∉ dom(Σ.L)` makes `b = a_emit` directly impossible (since `b ∈ dom(Σ.L)`), discharging the case in one line. The two-page detour through home equality, T4b's positional ranges, N/U/D field projections, and the two-branch K.λ construction is unnecessary.
**Required**: Use the freshness argument in Case II.A directly. The home-identity argument in Case II.B remains necessary (proper-prefix case), but Case II.A's mileage is gratuitous.

### Issue 8: Definition — FreshEmissionAddress is restated from ASN-0086
**ASN-0094, Definition — FreshEmissionAddress**: The definition restates ASN-0086's FreshEmissionAddress verbatim — same first/subsequent emission rule, same well-definedness via R0a-Cor1.
**Problem**: ASN-0086 already defines this. Restatement adds nothing.
**Required**: Cite ASN-0086's definition and drop the restatement.

### Issue 9: Definition — RelationalLayer paragraph mixes definition with motivation
**ASN-0094, Definition — RelationalLayer (in ASN-0086 foundation)**: This is in ASN-0086 already; the ASN-0094 framework's relational-layer scope is named at first use. The Nullify Compatibility section's "Supersession of ASN-0086's Nullify-as-sole-R-producer route" paragraph re-derives the compatibility — partially.
**Problem**: The section's heading suggests a compatibility analysis but the paragraph is a re-derivation of why Sh-conf admits Nullify and how it relates to ASN-0086's discipline. The substantive load-bearing claim is the *Corollary — NullifyActiveSubsetCompatibility*; the surrounding prose is exposition.
**Required**: Tighten Nullify Compatibility to the load-bearing corollary and one paragraph of context. The full discussion of audit-slice semantics vs set-semantics is referenced but not yet evaluated against a layer that needs both.

## OUT_OF_SCOPE

### Topic 1: Container-level link targeting (the `A_M` target-domain symbol)
**Why out of scope**: The Open Questions section flags this as a scope boundary item — extending the catalog with `A_M` for `dom(Σ.M)` addresses would re-enable metalink-style targeting. Belongs in a future ASN.

### Topic 2: Multi-process substrate concurrency
**Why out of scope**: The framework is explicitly committed to single-process substrates (Sh4 idempotency contract, Scope clause). Multi-process race semantics is a future extension.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: L9 admits ghost spans in endsets; the framework restricts slot positions to allocated addresses. Open Questions records this as a design choice for future ASNs.

### Topic 4: Higher-arity links (`|Σ.L(a)| > 3`)
**Why out of scope**: The framework's *Arity scope* clause explicitly restricts to the standard-triple slice. Extending shape components to higher arities is a separate framework extension.

### Topic 5: Cardinality vocabulary asymmetry (`1..*` not expressible)
**Why out of scope**: Open Questions flags the missing `1..*` token. Adding it would require either widening the cardinality vocabulary or composing existing shapes. Belongs in a future ASN that introduces a non-empty-slot use case.

VERDICT: REVISE
