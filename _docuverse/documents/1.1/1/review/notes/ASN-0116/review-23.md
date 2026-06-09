# Review of ASN-0116

The operational core is sound: the K.α→K.μ⁻→K.μ⁺→K.ρ decomposition is valid step-by-step, the shift arithmetic (`shift(q_k,n)=q_{k+n}`) discharges I-SHIFT/I-LEFT/I-NEW/I-DOM correctly, the provenance coupling (J0/J1★/J1'★/P7a) checks out, and the boundary cases (J=1, append, empty subspace) are handled. The range identity RAN and the P6 weakest-precondition computation (`D'=D∪Added`, equal iff `Added⊆D`) are correct. I found no technical hole. The remaining issues are accreted defensive/counterfactual prose flagged by the anti-bloat classifier.

## REVISE

### Issue 1: Counterfactual meta-commentary in P6
**ASN-0116, "A weakest precondition" section**: "Had P4 asserted unconditional preservation, this computation would have refuted it: `Added ∖ D(d, Σ)` is non-empty exactly when a ghost reference is resurrected..."
**Problem**: This imagines a refutation of a claim the ASN does not make. P4 already states the conditional form, so the counterfactual advances no reasoning — it is reviser drift commenting on a path not taken. The reader must skip it to reach the actual content (the two corollaries).
**Required**: Delete the counterfactual sentence; the containment wp stands on its own derivation.

### Issue 2: Defensive non-applicability paragraph for LP9
**ASN-0116, "A weakest precondition" section**: "Note this is *not* an instance of LP9 (ExtensionMonotonicity, ASN-0098): LP9 governs only K.μ⁺/K.μ⁺_L extension transitions, its proof rests on prior-domain agreement (E2...), which INSERT's I-SHIFT violates... and its conclusion is about `project`, not `ran`."
**Problem**: The derivation substitutes RAN into LP12 directly and never needs LP9. This three-clause explanation of why an unused lemma does not apply is accretion — it explains a non-step. It is the "imagines a case the precondition excludes" pattern at the lemma level.
**Required**: Remove the LP9 disclaimer; cite RAN and LP12 positively without pre-empting an inapplicable lemma.

### Issue 3: Defensive framing in P4 first bullet
**ASN-0116, P4 (LinkSurvival), "The link's target is unchanged"**: "We stress what does *not* underwrite this: it is *not* that `A_new` is fresh against `dom(C)`. Foundation L4/L9 let an endset reference *any* tumbler..."
**Problem**: The load-bearing fact (coverage-invariance rests on endset immutability via L12+LP3★, and ghost references are admissible) is genuine and must stay. But the contrastive "what does *not* underwrite this" framing is defensive accretion; the positive statement ("coverage-invariance rests on endset immutability, not freshness") carries the full content in one clause.
**Required**: State the basis positively and drop the "we stress what does not underwrite this" setup. Retain the L4/L9 ghost-reference point — it is needed by P4's new-block witnesses and P6.

## OUT_OF_SCOPE

The four Open Questions (transclusion-shared insertion point, concurrent-insertion freshness, transclusion provenance, post-edit fragmentation) are correctly deferred and not flagged as errors. No claims in the body stray into the retired-operation territory listed in scope.

VERDICT: REVISE
