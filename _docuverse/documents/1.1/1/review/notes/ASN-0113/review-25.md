# Review of ASN-0113

The mathematics is sound. I checked the load-bearing derivations — W4's exact-coverage via T5 prefix-confinement, W5's forward construction at the run's actual minimum (the T0(a)+S8-fin shared-prefix argument and the order-convexity converse), W10/W11's first-component confinement, W13's normalization, and the W20 weakest-precondition partition — and each holds, including the boundary instances (empty document → ⟨⟩, single-occupied-subspace, depth-2 collapse, depth-3 non-vacuous prefix confinement). No correctness defect found.

The findings are all the accreted meta-prose the `anti-bloat` classifier flags: forward-reference clustering, self-referential justification of phrasing, and counterfactual "why the axiom is needed" asides.

## REVISE

### Issue 1: Embedded out-of-scope inventory duplicates the external Scope block
**ASN-0113, "The substrate we measure"**: "We measure the document as a span-set, one member per kind; content delivery, region reads, the single overall bound (RETRIEVEDOCVSPAN), and the counting and discovery of individual links are out of scope."
**Problem**: This is a use-site/scope inventory sitting in reasoning prose. The same exclusions are already declared in the external Scope block (RETRIEVEV, RETRIEVEDOCVSPAN, FINDNUMOFLINKSFROMTOTHREE, FINDLINKSFROMTOTHREE). The sentence advances no claim; it restates the boundary the substrate paragraph had just finished establishing positively.
**Required**: Delete the clause after the semicolon. The positive statement "We measure the document as a span-set, one member per kind" is sufficient.

### Issue 2: Three paragraphs defer to W0 for the same empty-subspace case
**ASN-0113, W-pre / W5 / post-W5 paragraph**: W-pre — "legitimately yields the defined empty span-set `⟨⟩` (see W0)"; W5 — "the empty case is excluded ... and handled by W0"; the following paragraph — "The non-emptiness hypothesis excludes empty `V_S(d)`, which W5 does not cover and W0 handles separately".
**Problem**: This is the "multiple paragraphs defer to the same downstream location" pattern. The empty-subspace handling is pointed at W0 from three separate sites, each re-explaining the W-pre/W0 division of labor that W0 itself already states.
**Required**: State the empty/unallocated distinction once (at W-pre, where the precondition lives) and let W5's non-emptiness hypothesis stand without re-narrating that W0 covers the complement.

### Issue 3: W5 explains why its own phrasing was chosen rather than advancing the claim
**ASN-0113, W5**: "The existential is essential: the forward direction asserts that contiguity *permits* an exact span (a poorly chosen `σ` may overshoot even when `V_S(d)` is contiguous), while the converse asserts that non-contiguity *defeats every* `σ`."
**Problem**: This is meta-prose about the structure of the claim's quantifier, not part of the proof. The forward construction and the converse argument that follow already exhibit exactly this asymmetry; the sentence pre-explains them, so the reader processes the same content twice.
**Required**: Remove the sentence; the construction (forward) and the overshoot argument (converse) carry the asymmetry on their own.

### Issue 4: W18 parenthetical justifies why CL-UNIQ is needed instead of stating what it gives
**ASN-0113, W18**: "(Without CL-UNIQ a single link occupying two V-positions would double-count, and the member would not indicate the number of links at all.)"
**Problem**: This is the "new prose explains why the axiom is needed rather than what it says" pattern. The preceding sentence already states the load-bearing fact — CL-UNIQ makes `M(d)|V_{s_L}(d)` injective, giving the bijection. The counterfactual adds nothing the injectivity statement does not.
**Required**: Delete the parenthetical.

### Issue 5: W4 defensive parenthetical guards against a misreading rather than proving the step
**ASN-0113, W4**: "(The lower bound `start_S ≤ t` alone does *not* force this: lexicographic order is not componentwise order, e.g. `[S,2,1] ≥ [S,1,1]` despite its off-prefix second component; the confinement is the joint effect of both bounds via T5.)"
**Problem**: Defensive justification — it argues against a wrong proof a reader might attempt, rather than advancing the right one. The actual confinement step (T5 on both bounds) is already stated in the main sentence, and the depth-3 worked instance later exercises the same point concretely with `[S,2,1]`. The off-prefix counterexample appears in both places.
**Required**: Drop the parenthetical and rely on the depth-3 instance, which demonstrates the same exclusion non-vacuously.

## OUT_OF_SCOPE

None. The ASN correctly confines itself to the per-subspace extent query; the version-fork, transclusion, and overall-extent-consistency questions are properly left in Open Questions rather than claimed.

VERDICT: REVISE
