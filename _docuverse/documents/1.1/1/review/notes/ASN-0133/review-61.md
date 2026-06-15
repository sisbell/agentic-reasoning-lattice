# Review of ASN-0133

The mathematics is sound. I checked Q0's "audit always serves" rewrite against every constituent bucket (view-parameterized atoms rebuilt via `A_K`/`L_K` bases, fixed-view behavior atoms, `chain`'s unfiltered walk read natively at audit, the lone unsafe default-view-unfiltered-`chain` case correctly excluded); Q5's per-σ injection; Q5a's at-most-once bound and its open/closed asymmetry; Q6's three regimes including both necessity counterexamples (the holding-failure single-argument oscillation and the reaching-failure out-of-phase cycle, with H-SFAIR's regime form correctly closing the latter); and the cmt/res worked trace through `Sh-conf`/idem/extinction. The Marker-pattern dedup-impossibility argument (Q3) and the `target_of` "several"-re-arm (Q-FLIP) both hold. No correctness or completeness gap found. The findings below are prose-level, which is the register the active anti-bloat classifier asks for.

## REVISE

### Issue 1: Q0's worked example is placed after Q1
**ASN-0133, "Heterogeneous rewrite, worked." / "Value-preservation, at one state."**: both blocks sit between Q1's proof and "## Extinction discipline."
**Problem**: Their content is entirely Q0's — they construct and value-check the *fixed-view-base rewrite* that establishes `quiescent_R ∈ PL` for heterogeneous-view registries (the `R' = {ρ_walk, ρ_act}` construction, the naive-default/naive-active merges that fail at different conjuncts). Nothing in them concerns Q1's absorption. A reader following Q0's rewrite must skip past Q1's proof to reach the demonstration that the rewrite is value-preserving and required. Per the anti-bloat guidance, a concrete example in the wrong slot has its placement flagged.
**Required**: Move both blocks to immediately follow Q0, before Q1.

### Issue 2: H-SFAIR's nature is characterized in two places
**ASN-0133, H-SFAIR definition**: "It differs from H-FAIR not only in strength but in kind. H-FAIR's discharge is a disjunction … H-SFAIR is therefore a joint scheduler+environment condition, not a property of σ's scheduling alone: satisfying it in this regime requires the environment not to cycle any argument forever."
**ASN-0133, Q6**: "or the turn-fairness that strong fairness packages (the environment eventually leaving each argument in-domain and trigger-true at some scheduler turn, so it fires — H-SFAIR), two distinct routes (idleness versus cooperation)…"
**Problem**: The ~80-word "differs in kind" exposition in the definition is motivational essay content in a definition slot — the theorems consume only the *regime form* derived in the adjacent "Read through Q-EXT" sub-block ("no `(ρ,x)` is trigger-true at infinitely many indices"). Q6 then re-conveys the same environment-cooperation characterization at the point of use. The same property of H-SFAIR is explained twice.
**Required**: Keep the regime-form derivation (load-bearing) in the definition; let Q6's turn-fairness gloss carry the "joint condition / environment cooperation" intuition once. Consolidate, don't restate.

### Issue 3: Interpretive sentences that gloss definitions rather than advance them
**ASN-0133, RG**: "…the PL part is the trigger `T_ρ`, read at a single state, which the contract relates to those emission forms only as a registration-time obligation."
**ASN-0133, H-HOME**: "The fire definition's *some* emission set satisfying `Post_ρ` reads against this presupposition: where no registered home exists the fire has no admissible emission set…"
**Problem**: The flagged clauses explain *how to read* the surrounding definition (how `Post_ρ`'s type-status interacts with the trigger; how the fire definition's quantifier "reads against" H-HOME) rather than stating substrate content. The load-bearing statements survive their removal (Post_ρ is meta-level; a fire with no registered home has no admissible emission set, hence dischargeability is a standing hypothesis). These are small instances, but they are exactly the cross-referential meta-prose the classifier says compounds across cycles.
**Required**: Trim the interpretive clauses, keeping the bare statements.

## OUT_OF_SCOPE

### Topic 1: SF certification class, runtime divergence detector, scheduler construction
**Why out of scope**: The note's own deferrals are correctly scoped, not gaps to surface as REVISE. A `pd_extinct` (SF) certificate class (OQ1), a PL-expressible necessary divergence condition (OQ2), and the scheduler/serialization machinery discharging H-FAIR/H-ATOM ("What this note doesn't cover") are genuinely future or implementation-layer work. Flagging them as missing would be an error; the note proves consequences *under* these as named hypotheses, which is the right boundary.

VERDICT: REVISE
