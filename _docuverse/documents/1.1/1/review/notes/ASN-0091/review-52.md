# Review of ASN-0091

This ASN defines the abstract "Vstream-only" transition class, identifies REARRANGE_K as a realisation, and derives a battery of preservation consequences. The core mathematics is sound — I checked the worked-example arithmetic and the RE-ran/RE-μ/RE-frag derivations, and they hold. The problems are an unproven consequence presented as fact, one glossed identification, and very heavy accretion of redundant prose and examples (this note carries the `review-mode.anti-bloat` classifier, and the patterns are present).

## REVISE

### Issue 1: Fragmented-transclusion guarantee asserted but unproven, and contradicted by the Open Questions
**ASN-0091, "Cross-Document Transclusion Preserved"**: "it produces two contiguous V-intervals that *jointly refer to the same span at the source*."
**Problem**: No RE-* claim establishes that the two fragments of a split transcluded span "jointly refer to the same span at the source." RE-trans establishes only (i) range membership, (ii) multiplicity, (iii) home-document arrangement invariance — none of which states that the union of the two post-state I-intervals reconstitutes the original source span. Worse, the first Open Question asks precisely "What guarantees must rearrangement preserve about cross-document transclusion when a cut splits a span transcluded from the same source document into two non-contiguous pieces?" — so the body presents as established a guarantee the ASN's own Open Questions declare unresolved.
**Required**: Either promote this to a stated claim with an explicit derivation (the natural route is per-piece origin via the M16b-style argument plus a union-of-I-intervals lemma), or delete the assertion and let the Open Question stand.

### Issue 2: `x + 1 = inc(x, 0)` asserted without its validity precondition
**ASN-0091, inline lemma ChainDisjointAdjacency**: "The chain-adjacency successor `x + 1 = inc(x, 0)` preserves sub-allocator chain membership (TA5(c), ASN-0034)."
**Problem**: `x + 1` denotes `shift(x, 1)` (OrdinalShiftBase, ASN-0058) — an increment of the *last* component — while `inc(x, 0)` increments position `sig(x)`. These coincide only when `sig(x) = #x`, which holds for T4-valid addresses (TA5-SigValid) but not in general. The lemma is invoked on chain elements, which *are* T4-valid (ChainElementT4Validity), so the conclusion survives, but the equation is stated as if definitional. The same silent identification underlies every "`a_{i+1} = a_i + 1` within the chain" used to drive the run-decomposition witnesses (RE-frag/coal/eq).
**Required**: State the precondition once — chain elements are T4-valid, so `sig(·) = #·` and `shift(·,1) = inc(·,0)` — and cite it where the identification is used.

### Issue 3: Worked-example accretion — four of five examples re-verify the full RE-* battery
**ASN-0091, "Worked Example" ×3 plus "Two-Step Composition"**: each of the 4-cut Swap, Interior Cuts, and Two-Step examples re-discharges essentially the entire RE-C/L/dom/ran/μ/cov/disc/proj/frag/trans/sub/origin/R list plus a full RA-adm invariant sweep.
**Problem**: The review standard requires *at least one* concrete example; it does not license five. The 4-cut and interior-cut traces differ from the first only in which R-SPERM/R-EXT branch fires — that delta is one paragraph, not a full re-verification. Each example opens with a use-site justification ("To verify that each RE-* claim holds uniformly under…"), which is the exhaustiveness-claim bloat pattern. The reader must skip repeated identical RA-adm sweeps to reach the one new fact.
**Required**: Keep one full worked example. Reduce the 4-cut and interior-cut cases to the single distinguishing delta each (μ-region displacement; R-EXT firing on a non-empty exterior). The bijection-non-uniqueness example may stay since it demonstrates well-definedness, but trim its duplicate RA-adm sweep.

### Issue 4: The multi-step composition section is essay content over a "trivial induction"
**ASN-0091, "Composition Across Multi-Step REARRANGE Sequences" + the ★ table**: "the single-step claims compose by trivial induction."
**Problem**: By the ASN's own admission the composition is trivial induction; the section then spends a chaining lemma, a ~20-row ★ table restating every single-step claim verbatim with "compose by chaining," and a *second two-step worked example* (effectively a sixth full trace) to re-witness RE-frag★/coal★/eq★. The Two-Step example's three closing bullets ("Per-step pattern locality," "RE-ext as the bridging mechanism," "Pre-state staging permits both directions") are explanatory essay, not new reasoning.
**Required**: Replace the section with the chaining lemma, the per-fixed-document/per-V-position side conditions (which *are* substantive — RE-ext★ and RE-other★ genuinely need them), and a single sentence stating the ★ forms follow by induction. Drop the two-step worked example or reduce it to the staging argument alone.

### Issue 5: Independent re-derivation of foundation lemmas presented as new work
**ASN-0091, RE-proj / RE-cov / RE-disc derivations**: RE-proj is derived from scratch (RA-π + RE-cov) and then noted to be "governed by ASN-0098's LP11 (ReorderingBijection)"; RE-cov restates LP3; RE-disc restates LP12 + RE-ran.
**Problem**: RE-proj at the target document *is* LP11 with `Σ' = K.μ~(Σ)`. Deriving it again from RA-π and separately citing LP11 as the governing lemma is redundant and invites drift between the two statements. Same for RE-cov/LP3.
**Required**: State each as the operation-level instance of the foundation lemma ("RE-proj is LP11 specialised to REARRANGE_K"), and delete the parallel from-scratch derivation.

### Issue 6: Defensive meta-prose in the Provenance columns and clause-discharge notes
**ASN-0091, "Claims Introduced" Provenance column and clause-(iv) discharge note**: "an abstract-tagged claim, here and throughout, is one derived from the RA-* clauses alone, so it holds for every concrete realisation of the class"; "routing clause (iv) through RE-subpres would be circular, since the Layer-3 discharge of RA-adm itself presupposes clauses (i)–(v)."
**Problem**: The Provenance gloss re-explains the legend on multiple rows rather than tagging. The clause-(iv) circularity note is legitimate reasoning but is phrased as a defense of document ordering ("would be circular," "presupposes") — the anti-bloat target. The substantive content is "clause (iv) is discharged from R-PPERM/R-SPERM directly"; the circularity justification can be one clause.
**Required**: Move the Provenance legend to a single header sentence; compress the circularity note to its operative content.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: Open Question 2 correctly defers this; REARRANGE_K is content-subspace-only by CS3, and RE-sub frames the link subspace. New territory, not an error.

### Topic 2: Upper bound on run-decomposition cardinality increase
**Why out of scope**: Open Question 4. RE-frag establishes existence of increase; bounding it is a future quantitative result.

META: not applicable — the ASN defines a transition class, an operation, and state invariants at the right level of abstraction; it has not drifted into implementation mechanics, it has accreted redundant prose.

VERDICT: REVISE
