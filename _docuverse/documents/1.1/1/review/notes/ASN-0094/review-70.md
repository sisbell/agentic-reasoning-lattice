# Review of ASN-0094

## REVISE

### Issue 1: Missing "approved_by" walkthrough promised by Resolution catalog row
**ASN-0094, Canonical Shape Catalog (Resolution row) and Additional Worked Examples**: The Resolution row promises "A standalone use ... is exhibited at the 'Resolution base templates at a standalone K (no `_via` consumer in scope)' sub-walkthrough in *Additional Worked Examples* (`K = approved_by` registered with no parametric consumer in scope, exercising Emissions AB1, AB2, the AB3 rejection, and the full base-template evaluation table at Σ_2)".
**Problem**: No such sub-walkthrough exists in *Additional Worked Examples*. The only Resolution walkthrough present is "Resolution base templates exercised directly", which explicitly reuses Comment's `ρ_1`, `ρ_2` with Comment as a parametric consumer in scope — the opposite of standalone. No `approved_by` registration, no emissions AB1/AB2/AB3, no associated state Σ_2 appears anywhere in the document.
**Required**: Either add the promised `approved_by` walkthrough exhibiting standalone admissibility end-to-end, or rewrite the catalog row's parenthetical to reference what the document actually contains.

### Issue 2: Undefined "Sh5(b) per-row review checklist (steps 0–3)"
**ASN-0094, Resolution catalog row Standalone admissibility clause**: "passes the Sh5(b) per-row review checklist (steps 0–3) by hand-inspection."
**Problem**: No such numbered checklist is defined in Sh5(b) (which contains only a one-paragraph *Citation convention*). "Step 0 of Sh5(b)'s checklist" is referenced separately in the same row as "a new catalog row with shape tuple componentwise equal to R's must register `K_rep ~ R`". Steps 1, 2, 3 are not specified anywhere.
**Required**: Define the checklist with all four steps under Sh5(b), or rewrite the references to use the prose that actually appears in Sh5(b).

### Issue 3: Per-K discipline (FDD, SHCD) registration scope ambiguous across ~-classes
**ASN-0094, FunctionalDependencyDiscipline and SingleHomeCoverageDiscipline sub-sections**: Both disciplines say "A K registered with ... may additionally register" their discipline at K. The preservation theorems are stated per K ("Fix `K ∈ T_cat` with SingleHomeCoverageDiscipline registered at fixed home `d_K`").
**Problem**: `shape : T_cat → Shape` factors through `T_cat / ~` (per-class constancy), and `L_K^Σ = L_{K'}^Σ` whenever `K ~ K'`. But FDD/SHCD registration is described as per-K, not per-~-class. If `K, K' ∈ T_cat` with `K ~ K'` and only K is FDD-registered: emissions via `Emit_K` are FDD-gated, but emissions via `Emit_{K'}` are not gated, and both contribute to the same ~-class slice `L_K = L_{K'}`. A `Emit_{K'}` call could deposit a tuple with a from-slot matching a prior `Emit_K` tuple, breaking FDD's `from₁(τ) = from₁(τ') ⟹ addr(τ) = addr(τ')` conclusion at K. The framework's preservation theorems would fail at the ~-class slice they reason over.
**Required**: Either explicitly require per-~-class consistency for per-K disciplines (so registering FDD at K registers it at every `K' ~ K`), or rewrite the preservation theorems to handle mixed per-K registration within a ~-class. Same applies to SHCD (mixed `d_K` values across a ~-class would break the homed-set property uniformly over `L_K`).

### Issue 4: "Sh5(b) is a hand-followed convention" referenced as a labeled section that does not exist
**ASN-0094, Resolution catalog row Standalone admissibility clause and elsewhere**: "Because Sh5(b) is a design convention enforced by author diligence rather than by a tooled gate (see *Sh5(b) is a hand-followed convention*) ..."
**Problem**: No section, sub-section, or paragraph labeled "Sh5(b) is a hand-followed convention" appears in the document. The content is implied in Sh5(b)'s "by catalog-author diligence" wording but the labeled cross-reference target does not exist.
**Required**: Either label the relevant content (likely a sentence to add to Sh5(b)) with the cross-reference name, or replace the reference with the actual location/wording.

### Issue 5: Prose duplication on "per-shape uniformity" across catalog rows
**ASN-0094, multiple catalog row descriptions (DirectedPair, NonIdempotentDirectedPair, BundledDirectedPair, Provenance, Resolution, Retraction)**: Essentially identical paragraphs appear at each row claiming body-shape convergence with shape-mates is "hand-curated" not "framework-derived", with cross-references back to Sh5(a)'s *Status of per-shape uniformity (downgraded to aspiration in this draft)*.
**Problem**: Sh5(a) is itself one paragraph. Each catalog row restates Sh5(a)'s content in slightly different words while deferring to Sh5(a) for the canonical statement. This is the "multiple paragraphs in different sections defer to the same downstream location" pattern flagged in the forward-reference accretion note. Multiple rows say "the framework supplies no mechanical gate that would force the present body-shape choices to be the *only* admissible ones at this shape" or close paraphrases.
**Required**: State the per-shape uniformity convention once in Sh5(a) (with concrete content), then have catalog rows simply note "bodies hand-curated against the [shape-mate] row (Sh5(a))" without restating the convention.

### Issue 6: Sh4 contract has explicitly expository paragraph not consumed by any proof
**ASN-0094, Sh4 idempotency contract clause (i.a)**: "*Observe-step tightness (expository, under clause (d)).* When Sh-conf clause (d) admits the new emission (so `slot_addrs(F) ⊆ A^Σ`), Observe in (i.a) over-approximates exactly to `slot_addrs(F_τ) ⊇ slot_addrs(F)` ... This expository observation is not consumed by the contract's clauses (ii)/(iii) or by Sh4's preservation argument."
**Problem**: The paragraph self-declares that it is not consumed anywhere. By the reviser drift criterion, prose that does not advance the argument is noise. The "Contract correctness" paragraph that precedes it already establishes what is needed; the expository observation adds no load-bearing content.
**Required**: Remove the *Observe-step tightness (expository, under clause (d))* paragraph. If the AllocatedAddressAntichain-based reasoning is needed elsewhere, the AllocatedAddressAntichain lemma is already stated separately and citable.

### Issue 7: LinkAddressNotPrefixOfEmit proof contains meta-subsections commenting on proof structure
**ASN-0094, LinkAddressNotPrefixOfEmit proof**: The proof contains explicitly labeled meta-subsections: "*Identification of `origin(·)` and `home(·)` for the proof's scope*", "*FreshEmissionAddress branch forced under Case I*", "*Case-symmetry across Sub-cases 3a and 3b*", "*Dependence audit*", a "Worked examples — Cases I and II at concrete tumblers" subsection (running about a page).
**Problem**: Some of these aid the reader; others read as defensive accretion from prior review cycles (the *Case-symmetry* + *Dependence audit* combination is a "by symmetry" argument with a justification for the symmetry, appended atop the symmetry argument itself). The result is a proof that runs several pages for a structurally simple two-case statement. The "Worked examples" section at the end of the proof (giving concrete tumbler values to illustrate the case-split) is essay content in a structural slot — useful for pedagogy but adds substantial length without advancing the proof.
**Required**: Audit the proof for which subsections are load-bearing. The *Case-symmetry* and *Dependence audit* meta-subsections can collapse into a single "Sub-case 3b is symmetric to 3a; the disjointness predicate `s_L ≠ s_C` is symmetric" sentence. The worked-example illustration belongs in a separate "Examples" appendix if retained at all, not embedded in the proof body.

### Issue 8: Empty-baseline assumption stated as required for Sh4/FDD/SHCD but not surfaced as a scope boundary
**ASN-0094, Initial-State Baseline section**: "For Sh4/FDD/SHCD the empty-baseline `L_K^{Σ_init} = ∅` is required."
**Problem**: ASN-0086 admits reachable states from arbitrary initial configurations. The framework's preservation theorems for Sh4/FDD/SHCD depend on `L_K^{Σ_init} = ∅`. A layer instantiating the framework atop a substrate-conforming layer that does not start with empty link stores gets weaker guarantees than the framework states. This is a substantial scope restriction that affects whether the framework's theorems apply at all in such a layer; it should be visible in the Open Questions or in a *Scope boundary* tag, not buried as a precondition note.
**Required**: Add a scope-boundary item noting that the framework's preservation theorems apply only to layers starting from the empty-link-store initial state, and that retrofitting onto a non-empty initial state requires per-K verification of Sh4/FDD/SHCD baselines.

## OUT_OF_SCOPE

### Topic 1: Multi-process / distributed coordination of Sh4 contract atomicity
**Why out of scope**: The framework explicitly commits to single-process substrates (Sh4 contract *Scope: single-process substrate* clause, and Open Questions item on cross-process consistency). Extending to multi-process is correctly identified as out of scope.

### Topic 2: Container-level link targeting (`A_M` symbol)
**Why out of scope**: Open Questions enumerates this. The framework currently has no target-domain symbol for `dom(Σ.M)` addresses; extending the catalog is correctly flagged as future work.

### Topic 3: Composite shapes (relations whose slots are constrained by other relations' contents)
**Why out of scope**: Open Questions enumerates this. Not in the current canonical catalog.

VERDICT: REVISE
