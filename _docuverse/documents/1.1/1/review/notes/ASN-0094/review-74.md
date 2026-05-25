# Review of ASN-0094

## REVISE

### Issue 1: Sh4 contract's "Without the conditional hypothesis" sub-paragraph is imagined-case meta-prose
**ASN-0094, Idempotency (Sh4) section, *Sh4 idempotency contract* clause (i.a)**: "Without the conditional hypothesis (Sh-conf clause (d) fails on the new emission's pattern). Suppose `slot_addrs(F) = {d_unallocated}` where `d_unallocated ∈ T \ A^Σ`..."
**Problem**: The framework's Gate Ordering forces clause (d) to fire after gate 3 (the contract). The three-step walkthrough concludes: "Sh-conf clause (d)'s subsequent gate-4 rejection is what actually halts the emission in the unallocated-pattern case; the Sh4 contract at gate 3 sees an empty candidate set, fires clause (iii), and defers the rejection downstream." This is exactly the *imagining a case the claim's precondition already excludes* pattern — the argument doesn't establish independent contract correctness, it shows gate 4 catches a case the contract didn't filter.
**Required**: Replace the three-step walkthrough with one sentence ("post-filter (i.b) tests exact set-equality; slot_addrs(F_τ) ⊆ A^Σ by Sh2 excludes unallocated patterns, yielding C = ∅"), or remove the imagined case.

### Issue 2: Initial-State Baseline section bloats one assumption into four overlapping paragraphs
**ASN-0094, Initial-State Baseline section**: Four paragraphs (*Initial-state baseline for preservation proofs*, *Global empty-link-store assumption*, *Scope of the per-tuple-conformance relaxation*, *Per-walkthrough convention*) all discuss what the framework assumes at Σ_init.
**Problem**: The substantive content is one sentence: "Sh0–Sh4 presuppose L_K^{Σ_init} = ∅ for K ∈ T_cat; walkthroughs additionally assume dom(Σ_init.L) = ∅." The other three paragraphs are meta-prose explaining what's not enough for what (Scope), what walkthroughs do (Global), and what conventions repeat per walkthrough.
**Required**: Consolidate to one paragraph stating the baseline and one sentence stating the walkthrough convention.

### Issue 3: Caller-side rejection classification duplicates the Gate Ordering enumeration
**ASN-0094, The Conformance Axiom section, *CallerSideClassification* Definition and *Gate Ordering (consolidated)* Definition**: Six caller-side checks aligned with five consolidated gates, with explicit cross-mapping ("Registry check (#1) is implicit in the consolidated Gate Ordering...", "Cardinality check (#5) and Target-domain check (#6) together correspond to consolidated gate 4...").
**Problem**: Two enumerations describing the same gate sequence with different numbering, bridged by a paragraph explicitly cross-mapping them. This is the *multiple paragraphs deferring to the same downstream location* pattern.
**Required**: Pick one enumeration as primary. If callers need fine-grained classification, the consolidated gates can be the canonical statement with caller-side dispatch as a one-paragraph note.

### Issue 4: RetractionSelfFreshness's *Use sites* paragraph enumerates downstream consumers
**ASN-0094, Lemma — RetractionSelfFreshness section**: "*Use sites.* The lemma is cited by Sh4's preservation argument at: Case C — to rule out the K ~ R self-retraction sub-case...; Case D — to establish the structural pivot..."
**Problem**: The lemma's section enumerates where it will be cited downstream, and then compares the lemma to NullifyActiveSubsetCompatibility ("The Nullify Compatibility section's Corollary uses R0a at Σ' directly..."). The lemma's content doesn't depend on which consumers exist. This is the *enumerate downstream consumers* pattern. The Properties Introduced table's "hoisted as a top-level section before Sh4" further compounds with the *prose justifies document ordering* pattern.
**Required**: Remove the *Use sites* paragraph and the comparison-with-NullifyActiveSubsetCompatibility paragraph. Remove "hoisted as a top-level section" from the Properties Introduced row. Downstream consumers cite the lemma where they need it.

### Issue 5: No concrete walkthrough exercises FDD or SHCD
**ASN-0094, Worked Example section and Per-Shape Template Walkthroughs**: The walkthroughs exercise Classifier, BundledDirectedPair (`citation.depends`), NonIdempotentDirectedPair (`comment`, with "no SHCD opt-in registered"), and Resolution (as the parametric `K_res` argument).
**Problem**: The framework introduces three layer-discipline contracts (Sh4 idempotency, FDD, single-home commitment) with preservation theorems and consumer-facing accessors (`K_target_of`, `latest_K_for_addr`). FDD and SHCD are described only in definitional prose. The review guidance says "no concrete example" is a REVISE item; the framework's two non-Sh4 disciplines lack any concrete verification.
**Required**: Add a worked example exercising FDD (the singleton-returning `K_target_of` with at least one suppression-by-clause-(ii) and one ⊥-handling at empty candidate set) or SHCD (a `latest_K_for_addr` evaluation with `emission_order` over a chain of emissions). The walkthrough should include the per-K-discipline suppression pattern explicitly.

### Issue 6: Sh5 is labeled META but has no operational content
**ASN-0094, Template Catalog (Sh5) section**: "Sh5 is an organizational convenience for hand-curating the canonical shape catalog; it is not a mechanical-derivation theorem."
**Problem**: Sh5's body has three sub-paragraphs: (a) per-shape uniformity is an aspiration (downgrade), (b) signature derivation rule (mechanical), (c) citation convention (catalog-author diligence). None are framework theorems — they are editorial conventions. Labeling them as a numbered property suggests theorem-status that doesn't exist.
**Required**: Demote to a paragraph titled "Catalog Curation Discipline" or fold sub-paragraph (b) into the canonical catalog table's preamble. Remove the META label since it labels organizational discipline rather than a framework property.

### Issue 7: Decidability of coverage-equality is essay content embedded in TypedRelationCatalog Definition
**ASN-0094, Shape section, *Definition — TypedRelationCatalog***: The *Decidability of coverage-equality on finite span sets* sub-paragraph derives a four-step algorithm with complexity analysis embedded in the definition.
**Problem**: The decidability claim is needed by the registry's membership test, but the full algorithm and complexity analysis belong in a separate lemma. The Definition's primary content is "T_cat ⊆ T_admissible, finite up to ~, closed under ~"; the decidability machinery overweights the definitional content.
**Required**: Extract the four-step algorithm into a separate lemma (e.g., "Lemma — CoverageEqualityDecidability"). Leave the Definition with a one-sentence claim pointing at the lemma.

### Issue 8: Framework-wide commitment paragraph is meta-prose
**ASN-0094, Scope and Substrate Scaffolding section, *Framework-wide commitment to the subspace_I(·) = E(·).1 identification* paragraph**: "The identification surfaced by the subspace partition clauses above is adopted as a framework-wide invariant: every theorem, lemma, definition, template, and worked example below operates under it..."
**Problem**: The paragraph states "we use this assumption everywhere" — already implied by the assumption being a framework scaffolding clause. The downstream enumeration ("every theorem, lemma, definition, template, and worked example") is the *enumerate downstream consumers* pattern at the scaffolding-clause level.
**Required**: Fold the identification into the Link/Content subspace partition scaffolding clauses themselves; remove the separate paragraph.

### Issue 9: Lifetime constancy paragraph explains why the axiom is needed rather than what it says
**ASN-0094, Shape section, *Lifetime constancy of T_cat* paragraph under Definition — TypedRelationCatalog**: "The lifetime constancy is required for the inductive baselines of Sh0–Sh4 to discharge uniformly. Each induction begins with 'At Σ_init, every L_K^{Σ_init} = ∅...' A K admitted to T_cat only after some prior states have elapsed would face a non-vacuous baseline at its registration point..."
**Problem**: The paragraph explains why constancy is necessary rather than stating constancy concisely. The justification-as-content reading is the *new prose around an axiom explains why the axiom is needed rather than what it says* pattern.
**Required**: Replace with a one-sentence axiom: "T_cat is fixed at Σ_init and does not change as states evolve." Move the inductive-baseline argument into the Sh0 proof's preamble, where it's actually consumed.

## OUT_OF_SCOPE

### Topic 1: Multi-process consistency for Sh4/FDD/SHCD contracts
**Why out of scope**: The three layer-discipline contracts commit to single-process substrates. Multi-process coordination protocols at the ~-equivalence class scope are flagged in Open Questions; this is a framework-scope boundary, not an internal gap.

### Topic 2: Mechanical body-derivation from shape components
**Why out of scope**: Sh5(a) explicitly downgrades body convergence at shape-mates to hand-curation. A future ASN could introduce mechanical body-derivation; the current framework's scope is signature derivation only.

### Topic 3: Container-level link targeting (A_M)
**Why out of scope**: Target-domain vocabulary admits {A_doc, A_rel, A, -} only. Extending to A_M (dom(Σ.M)) for metalink-style targeting is a framework extension, flagged in Open Questions.

VERDICT: REVISE
