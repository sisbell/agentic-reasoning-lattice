# Review of ASN-0087

I worked through the composite definition, the precondition/effect derivations, the wp computation, the worked example, and the full invariant-preservation accounting. The mathematics is sound: every conjunct of ASN-0047's per-state invariant package is addressed, the boundary cases (empty endset slots, first link with `V_{s_L}(d) = ∅`, reflexive coverage, removed `v_ℓ`) are covered, and the worked example checks discoverability concretely against length-8 tumblers. The S2 derivation correctly splits into within-subspace and cross-subspace exclusions rather than hand-waving `v_ℓ ∉ dom(M(d))`. The findings below are anti-bloat / prose items, consistent with the `review-mode.anti-bloat` classifier on this note.

## REVISE

### Issue 1: Design-rationale meta-prose in the StandardAuthoring definition

**ASN-0087, Inputs (Standard authoring)**: "coverage intersected with `F` … (the only set K.α and K.λ allocate from, with `dom(Σ.C) ∪ dom(Σ.L) ⊆ F` by LP-Sub; **intersecting with `F` keeps the condition non-vacuous against the finite stores C-fin, L-fin**)"

**Problem**: The bolded clause justifies *why the definition is shaped this way* (to avoid an unsatisfiable subset condition over infinite prefix coverages) rather than advancing the definition's meaning. This is the "defensive justification" anti-bloat pattern. The two preceding facts (F is the allocation set; `dom(C) ∪ dom(L) ⊆ F`) are load-bearing; the vacuity-avoidance gloss is not.

**Required**: Drop the "keeps the condition non-vacuous against the finite stores" clause; retain only the substantive facts that `F` is the allocation set and contains the stores.

### Issue 2: Threefold restatement of composite non-atomicity

**ASN-0087, Atomicity**: The section opens "MAKELINK is a composite of two atomic transitions… The composite is not." It then closes with "The substrate provides no composite-level atomicity… Composite-level atomicity is not a substrate guarantee." — two sentences in the closing paragraph asserting the same proposition, bracketing a single intervening observation. M-CompAtomicity then states it a third time ("The composite is not atomic at the substrate level").

**Problem**: "Two paragraphs … say the same thing in different words." The claim that the composite is not atomic is made at the section head, twice in the closing paragraph, and again in the claims table.

**Required**: State composite non-atomicity once in the prose (anchored to SequentialTransitionAxiom giving only per-step atomicity) and once in the M-CompAtomicity row; remove the redundant closing restatement.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets (Open Question 1)
**Why out of scope**: The constraints on endsets whose spans cover not-yet-allocated addresses are correctly deferred — StandardAuthoring is offered as a discipline, and the side-effect/Resurrection analysis already characterizes the consequence. The enforced constraint belongs to a future authoring-discipline ASN.

### Topic 2: Protocol-level visibility bound on `Σ_mid` (Open Question 5)
**Why out of scope**: The ASN correctly states the substrate offers no composite atomicity and locates any visibility guarantee in a protocol layer above the substrate; that is genuinely new territory, not a gap here.

VERDICT: REVISE
