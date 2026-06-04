# Review of ASN-0091

This ASN is technically sound — the abstract Vstream-only class, its REARRANGE_K realisation, the RE-* claims, and all four worked examples check out under scrutiny (I verified the fragmentation/coalescence/equality run arithmetic, the ChainDisjointAdjacency lemma, the LP-Fin coverage computations, and the net-effect split's collapse witness). The findings below are the meta-prose and forward-reference accretion this note's `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Bijection non-uniqueness stated three times
**ASN-0091, "REARRANGE as Vstream-Only Operation" and "Projection Transports Along π"**: The opening section already states "It is not in general unique: when Σ.M(d) has shared I-addresses... the assignment within each such block is free." The RE-proj *uniform formulation* restates it: "This identity is well-defined across the freedom in choosing π: when Σ.M(d_tgt) carries shared I-addresses... multiple bijections satisfy RA-π, yet the set image... regardless of which witness is used." The fourth Worked Example then demonstrates it concretely.
**Problem**: Two abstract prose statements of the same fact in different words; the concrete demonstration (the Worked Example) is the one that earns its place. The two prose statements are redundant.
**Required**: State the non-uniqueness once (the opening), and let the Worked Example carry the well-definedness demonstration. Drop the RE-proj uniform-formulation restatement, keeping only the π̂_d definition it needs.

### Issue 2: Dependency-inventory appended to the S2 derivation
**ASN-0091, "REARRANGE as Vstream-Only Operation" (S2 derivation)**: "The derivation is abstract — it relies only on RA-dom, RA-π (bijection), and pre-state S2 at Σ (used pointwise at each v to license 'function value' on the right-hand side)."
**Problem**: This sentence re-enumerates the premises just used rather than advancing the proof — a use-site inventory in a proof slot. The derivation already cited each premise inline.
**Required**: Delete the trailing sentence.

### Issue 3: Inline forward-reference pointers
**ASN-0091, multiple sections**: "RA-frame's other-document clause (the same equality later catalogued as RE-other)"; "Define the projection transport π̂_d analogously to the multi-step π̂ of the composition section below"; the fragments-reconstitute aside "is left to the first Open Question."
**Problem**: These point the reader forward to content not yet stated to justify a step in place — the forward-reference accretion pattern. RA-frame's clause stands on its own without the "later catalogued as RE-other" pointer; π̂_d is defined locally and does not need the "analogously to... below" gloss.
**Required**: Remove the inline forward pointers; cite the clause/definition directly where used.

### Issue 4: Net-effect split's why-no-constraint defensiveness
**ASN-0091, "Clause Correspondences and Per-Invariant Discharges" (Net-effect split)**: "admissible because R-PRE imposes no net-effect requirement — the realiser is the unbundled elementary sequence K.μ⁻ + K.μ⁺, each step independently valid (neither K.μ⁻'s per-subspace retention count nor K.μ⁺'s content-store-membership-plus-shape precondition carries a net-effect requirement)."
**Problem**: The parenthetical justifies the *absence* of a constraint by inventorying two preconditions that lack it — defensive prose explaining why no obstacle exists rather than advancing the realisation argument.
**Required**: State that the collapse case yields Σ' = Σ and is realised trivially; drop the precondition inventory.

### Issue 5: Prose restating the discharge tables
**ASN-0091, "Clause Correspondences and Per-Invariant Discharges"**: "With clauses (i)–(v) closed by the table above, REARRANGE_K's π is an admissible K.μ~ bijection in the non-trivial case, where the realiser is the valid composite K.μ⁻ + K.μ⁺."
**Problem**: The table already supplies clause→discharge for (i)–(v); this sentence restates the table's conclusion. It also wobbles terminology — "the valid composite K.μ⁻ + K.μ⁺" here versus "the named composite K.μ~" in the net-effect split (the same object, named two ways within a page).
**Required**: Either keep the table and drop the restating sentence, or fix the terminology to one consistent name for the realiser.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: The ASN correctly confines REARRANGE_K's cut subspace to s_C (CS3) and defers link-subspace reordering semantics to Open Question 2. This is proper scoping, not a gap.

### Topic 2: Fragment reconstitution of a split same-source span
**Why out of scope**: Whether two fragments of a transcluded span jointly reconstitute the source is correctly deferred to Open Question 1 — new territory, not an error here (modulo the inline-pointer flag in Issue 3).

VERDICT: REVISE
