# Review of ASN-0036

The mathematics here is solid — I checked the within-subspace incompatibility lemma (both `j < m` and `j = m` branches), the cross-subspace T5/T10 argument, OrdAddHom's three-region case analysis, D-CTG-depth's infinite-intermediates construction, and D-SEQ's four-step assembly. All hold. No cross-ASN violations: every external reference is to ASN-0034 (foundation). My findings are confined to the anti-bloat mandate this note carries, plus one clarity defect.

## REVISE

### Issue 1: S8a triple-states the definitional/derived split
**ASN-0036, S8a**: The distinction "`zeros(v) = 0` and `#v ≥ 2` are definitional, only componentwise positivity is derived" is stated in the prose intro ("From this structural commitment the zero-count and componentwise-positivity conjuncts follow"), restated in full in the proof ("The depth `#v ≥ 2` and the field-separator-free property `zeros(v) = 0` are definitional"), again in the Definition slot ("both definitional: they unfold directly from..."), and a fourth time in the Postconditions slot ("where `#v ≥ 2` and `zeros(v) = 0` are both *definitional*... and only componentwise positivity... is *derived*").
**Problem**: The same epistemic bookkeeping ("which conjunct is axiomatic vs. proved") is repeated four times across slots. A precise reader must re-read the same caveat to confirm it is the same caveat. This is the "new prose around an axiom explains... rather than what it says" pattern.
**Required**: State the definitional/derived split once (the proof is the right home) and let the Definition/Postconditions slots state the conjuncts plainly.

### Issue 2: Duplicate boundary-collapse paragraph in OrdAddHom and OrdAddS8a
**ASN-0036, OrdAddHom proof and OrdAddS8a proof**: Both proofs contain a near-verbatim paragraph: "The boundary regimes of `k` collapse one or both copy regions to the empty range: at `k = 2`, the [first/middle] range... reduces to... and is empty...; at `k = m`, the [third/trailing] range... reduces to... and is empty..."
**Problem**: Two paragraphs in different sections saying the same thing — the action-point boundary collapse is a property of TumblerAdd's three-region formula and need not be re-argued per lemma.
**Required**: Argue the boundary collapse once (or cite it as a TumblerAdd consequence) and reference it from the second site.

### Issue 3: "Orphaned content persists / S0 forbids reclamation" stated three times
**ASN-0036, S3 Frame + asymmetry paragraph + Persistence independence section**: The S3 Frame says "orphaned content; S0 forbids reclamation, so orphaned content persists." The asymmetry paragraph after S3 repeats it via Nelson's "deleted bytes." The entire "Persistence independence" section then re-derives it: "Content therefore persists in Istream whether or not any arrangement references it: S0 forbids reclamation."
**Problem**: One consequence of S0 (unreferenced content is not reclaimed) occupies three separate slots with no new content added past the first.
**Required**: Consolidate to one statement. The standalone "Persistence independence" section adds nothing beyond the S3 Frame note and can be folded in or removed.

### Issue 4: S8 image-corollary's run-specific clause is vacuous for the proven decomposition
**ASN-0036, S8 Postconditions (Corollary)**: "...in particular, for any correspondence run `(vⱼ, aⱼ, nⱼ)`, every step image `shift(aⱼ, k)` with `1 ≤ k < nⱼ` inherits these properties."
**Problem**: The existence proof establishes only the *singleton* decomposition (every `nⱼ = 1`), for which the range `1 ≤ k < nⱼ` is empty — so the "in particular, for any correspondence run" clause refers to step images the proven decomposition never produces. The corollary already states the load-bearing fact pointwise ("The fact holds on `dom(Σ.C)` independently of any run cardinality"); the run-specific restatement adds confusion, not content.
**Required**: Drop the run-specific clause and keep only the pointwise statement on `dom(Σ.C)`, or prove a non-singleton (maximal) decomposition so the clause is non-vacuous.

### Issue 5: Use-site inventories in the local-property Depends slots
**ASN-0036, S8 / D-SEQ / D-CTG-depth Depends**: The "(*Local properties*)" groupings narrate where each dependency is consumed step-by-step — e.g., S8: "S8a — supplies `zeros(v) = 0` and `#v ≥ 2` for the within-subspace incompatibility lemma..."; D-SEQ: "D-CTG — supplies Step 3's contiguity-of-k-values argument...", "D-MIN — supplies Step 1's identification... and Step 2's `k = 1` base case."
**Problem**: This is the use-site-inventory pattern: the Depends slot re-narrates the proof body rather than naming what each dependency provides. The step-by-step consumption is already legible in the proof.
**Required**: Reduce each Depends entry to the claim it supplies; drop the "supplies Step N's..." cross-references, which duplicate the proof structure.

### Issue 6: Formulaic "design requirement, not a convention" repetition
**ASN-0036, S7a / S7d / S8-depth / D-CTG-depth context**: The phrase "This is a design requirement, not a convention" (and "parallel to S7a") recurs across S7a, S7d ("a design requirement parallel to S7a"), and S8-depth ("a design requirement, not a convention — parallel to S7a").
**Problem**: The "design requirement" status is already carried in each Formal Contract's "*Axiom (design requirement)*" label; the repeated prose assertion plus the "parallel to S7a" back-references add no reasoning.
**Required**: Drop the prose status-assertions; the axiom label already conveys it.

## OUT_OF_SCOPE

### Topic 1: "Basic INSERT typically commits to m = 2"
**Why out of scope**: The ValidInsertionPosition/ValidFirstInsertionPosition predicates are legitimate state-level characterizations of valid arrangement positions, derived from D-MIN/D-SEQ/contiguity. But the remarks tying depth choice to "Basic INSERT" are operation-specific (INSERT mechanics are out of scope). The predicates themselves stay; the operation-naming is already correctly routed to the open questions.

VERDICT: REVISE
