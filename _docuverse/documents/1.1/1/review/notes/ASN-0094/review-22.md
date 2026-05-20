# Review of ASN-0094

## REVISE

### Issue 1: Forward reference in EffectiveWpSimplification

**ASN-0094, EffectiveWpSimplification Corollary**: "By Sh1 at `K := R`, `G'` is canonical-slot with `match(|slot_addrs(G')|, 1)`... By Sh3 at `K := R`, `slot_addrs(G') ⊆ t_G^Σ = A_rel^Σ = dom(Σ.L)`."

**Problem**: The corollary's proof depends on Sh1 and Sh3, but these are proved several sections later. The author addresses this with an "anticipation note" claiming acyclicity (which is correct — Sh0–Sh3 don't consume the corollary). However, the document organization places a proof site before its consumed lemmas, forcing the reader to trust the forward reference. The "anticipation note" prose is a hedge, not a fix.

**Required**: Either (a) move EffectiveWpSimplification to after the Target Domain section (after Sh1 and Sh3 are proven), or (b) restructure the framework as a stratified construction with an explicit dependency diagram showing the proof-order: Sh-conf axiom → Sh0–Sh3 inductions → EffectiveWpSimplification corollary → Sh4 induction. The acyclic dependency should be evident from the document's order, not require trust in a forward-reference disclaimer.

### Issue 2: Sh-conf section is overloaded

**ASN-0094, "The Conformance Axiom" section**: The section contains nine substantial subdivisions — the axiom definition, justification, scope, three paragraphs on Nullify interaction, compatibility with ASN-0086's Nullify postcondition, two paragraphs on the initial-state baseline, scope of the per-tuple-conformance relaxation, the RetractionTargetNotOnChain Lemma (with multi-step Case II proof), and the EffectiveWpSimplification Corollary.

**Problem**: Loading nine substantive items into one section makes it hard to verify each independently. A reader checking RetractionTargetNotOnChain's Case II zero-count additivity argument must scroll past axiom prose, supersession discussion, and baseline-relaxation analysis.

**Required**: Split into separate sections: (a) Sh-conf definition and justification; (b) Interaction with Nullify (Nullify compatibility, supersession of ASN-0086's restriction); (c) Initial-state baseline (could be moved to Preliminaries); (d) RetractionTargetNotOnChain as its own lemma section; (e) EffectiveWpSimplification as its own corollary section after Sh1/Sh3.

### Issue 3: Catalog row naming mixes structural and semantic conventions

**ASN-0094, "The Canonical Shape Catalog" table**: Rows are named with mixed conventions — structural (DirectedPair, NonIdempotentDirectedPair, Tuple-Classifier) and semantic (Classifier, Resolution, Retraction, Provenance).

**Problem**: The author explicitly says "Naming conventions are layer constructs, not catalog rows" but uses semantic names for some catalog rows. A reader looking for the canonical name for `(1, 1, A_doc, A_rel, ⊤)` finds "Resolution," but the analogous `(1, 1, A_doc, A_doc, ⊤)` is "DirectedPair." Why not "Tuple-DirectedPair" for consistency with Tuple-Classifier?

**Required**: Either (a) commit to structural naming throughout (rename Resolution → "DirectedTupleTarget" or similar; rename Retraction by its shape pattern), or (b) document the naming policy explicitly — when does the catalog use semantic vs structural names, and why? The current state suggests historical accretion rather than a deliberate choice.

### Issue 4: SharedDepthOneAllocator lemma's role in ASN-0094 is unclear

**ASN-0094, "Scope and Substrate Scaffolding" section**: SharedDepthOneAllocator is referenced as a foundation-provided lemma from ASN-0086.

**Problem**: I traced its consumption within ASN-0094 and found no load-bearing use. It's not cited in any Sh0–Sh4 proof, not consumed by RetractionTargetNotOnChain, and not used in the walkthroughs. If the lemma is foundation context provided for orientation but not consumed, the framing should make this clear.

**Required**: Either explicitly cite SharedDepthOneAllocator at the proof site where it's consumed (if it is consumed somewhere I missed), or note in the scaffolding section that it's contextual rather than load-bearing.

### Issue 5: Sh5(b) discipline relies on per-row hand-checking

**ASN-0094, Sh5 META status**: "*META discipline.* This framework's catalog adheres to the rule that every catalog row's templates depend only on the following four input categories..."

**Problem**: The catalog-wide citation audit table is a hand-curated check that each row passes the discipline. There's no mechanical procedure to verify a new row complies — adding a row requires the author to audit every template against the four categories. Sh5 itself acknowledges this is META, but the discipline's enforceability rests entirely on reviewer attention.

**Required**: Either (a) state explicitly that catalog extension is a manual review process subject to the discipline (acknowledged as the cost of Sh5's META status), or (b) introduce a derivation procedure for template bodies from shape components — even if hand-applied, a procedural recipe would make discipline violations mechanically detectable.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrates with concurrent Sh4-emitters
**Why out of scope**: The framework explicitly scopes itself to single-process substrates; the Open Questions section flags cross-process consistency as not addressed. Extending Sh4's atomicity scope across processes requires a distributed coordination protocol beyond this framework's commitments.

### Topic 2: Bipartite expansion to Tuple-DirectedPair, Tuple-Resolution, etc.
**Why out of scope**: The catalog notes that further bipartite entries (link-side analogs of document-side shapes) can be added by extending the catalog. The current enumeration is intentionally restricted to present-day predicate templates.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: Sh-conf clause (d) rejects unallocated slot addresses. L9 (TypeGhostPermission, ASN-0043) admits ghost spans generally. Whether a future shape family should admit ghost-targeting slot semantics under a state-dependent conformance rule is an open design question flagged in Open Questions.

### Topic 4: Runtime extension of T_cat
**Why out of scope**: T_cat is fixed at Σ_init. Layers wanting to introduce new typed relations must declare them at Σ_init or face the burden of verifying empty-baseline at registration. This restriction is acknowledged.

VERDICT: REVISE
