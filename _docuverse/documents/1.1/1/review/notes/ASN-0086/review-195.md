# Review of ASN-0086

I checked the core proofs (R0, R0a, R-Scope, R6a–d, R7a, the wp analyses) and the worked sketch against the foundations. The reasoning is sound — I found no correctness defect in the relational-layer guarantees. The findings below are the forward-reference accretion and meta-prose the `review-mode.anti-bloat` classifier targets, which a precise reader must work around.

## REVISE

### Issue 1: Remark — NestedLinkWitness mutually forward-defers with Emit_K
**ASN-0086, Remark — NestedLinkWitness**: "Consequently `Emit_K` is undefined at such a state: were the non-frontier nested key the apparent `ℓ_prev` at home `d`, the subsequent-emission `inc(ℓ_prev, 0)` would be off-chain..."

**Problem**: This Remark sits in *The Two Foundational Sets*, but its closing sentence forward-references `Emit_K` (defined pages later in *Three Operations*) and `R0a` (defined later in *Tuple Identity*). Emit_K's own definition then defers back: "partial over the broader state-local-conforming sub-space, undefined exactly where the chain frontier is ill-formed (Remark — NestedLinkWitness)." This is a circular deferral — two sections in different locations each pointing to the other to explain Emit_K's partiality. The Remark's load-bearing content is purely structural: a nested pair `a ≼ a''` satisfying the state-local L/S-invariants yet violating the eventual antichain. That structural fact stands on its own.
**Required**: Confine the Remark to the structural witness (state-local-conforming ⊋ substrate-conforming). State Emit_K's undefinedness once, at Emit_K's definition, where partiality is the topic.

### Issue 2: wp Case 2 load-bearingness restates its derivation as a preview
**ASN-0086, Weakest-Precondition Analysis, "Domain restriction"**: "Both restrictions are load-bearing, and the `a ∉ nullified(Σ')` step of the derivation below consumes both: (i) substrate-conformance, via R0a's antichain; (ii) the unit-depth retraction discipline."

**Problem**: The "(i)/(ii) consumes both" preview duplicates the *Derivation (both directions)* paragraph, which states the same consumption verbatim ("supplies, via (i), substrate-conformance... By unit-depth-disciplinedness of Σ (domain precondition (ii))"). Between the preview and the derivation sit two dedicated insufficiency paragraphs ("Substrate-conformance alone is insufficient", "The discipline alone is insufficient"). The section announces, then separately proves each, then re-derives — four passes over a two-restriction claim.
**Required**: Drop the preview's "(i)/(ii) consumes both" sentence; let the Derivation carry the consumption. The two insufficiency paragraphs are the load-bearingness proof; the announcement is redundant.

### Issue 3: Definition — relational layer digresses into "sufficient not equivalent"
**ASN-0086, Definition — relational layer**: "Confinement to P1-satisfying Nullify calls is *sufficient* for the discipline but not equivalent to it... the converse fails — a direct `Emit_R` whose target `t ∉ A_rel`... (e.g. Worked Sketch Step 4...) ... yet once `t` enters `A_rel` ... still satisfies the per-state unit-depth predicate. This routing is thus one sufficient strategy, not the only configuration the per-state predicate admits."

**Problem**: This is an extended aside characterizing configurations the layer *does not* use, with a forward reference into Worked Sketch Step 4. It does not advance the layer's definition (operation set + discipline commitment); it speculates about the boundary of a predicate the layer never reaches. Essay content in a structural slot.
**Required**: State that the layer routes all `R`-typed emission through P1-confined `Nullify` and thereby satisfies the unit-depth discipline. Delete the sufficient-vs-equivalent excursion.

## OUT_OF_SCOPE

### Topic 1: Concurrency, atomicity, ordering, and cardinality bounds on retraction
**Why out of scope**: The Open Questions (Observe/Emit atomicity, observation ordering, `|nullified(Σ)|` bounds) concern a concurrency and observation model the substrate does not yet fix. They are correctly deferred — this note specifies the single-threaded `→`/`↝` relational layer, not its consistency model.

### Topic 2: Multi-arity typed relations `L_K^{(n)}`
**Why out of scope**: The note explicitly restricts to standard triples (`|Σ.L(a)| = 3`). Higher-arity links exist in `dom(Σ.L)` but the relational construction over them is named as future work, not an omission here.

VERDICT: REVISE
