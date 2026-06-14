# Review of ASN-0131

The operation is well-specified and the underlying mathematics is sound. I checked the core definition, the worked instance, union/intersection distributivity, the contraction weakest precondition (RE-CWP), fresh-output addressability (RE-ADDR), and retraction stability (RE-RET) line by line — all hold. The note also meets the depth standards: a concrete worked example exercising every distinctive postcondition, a non-trivial wp (RE-CWP), and explicit derivations for the "derived" claims (RE-SEL, RE-TRANS, RE-IDENT).

The findings below are accretion, not correctness — which is the point of an anti-bloat cycle. They are the meta-prose a reader has to work past.

## REVISE

### Issue 1: Redundant second justification + forward reference for link-only K.μ⁻ stability
**ASN-0131, "Stability" section, link-subspace-confined edits paragraph**: "The contraction case is RE-CWP's `Δ = ∅` instance — no content position is dropped, so `I_R = image(W, d, Σ)` and `Δ = ∅`."
**Problem**: The paragraph has *already* proven link-only K.μ⁻ leaves the answer fixed directly — "retained-position agreement gives `W ∩ dom(Σ'.M(d)) = W ∩ V_{s_C}(d) = W ∩ dom(Σ.M(d))`, so `image(W, d, Σ') = image(W, d, Σ)`" — and concluded "Either edit gives `RE(W, d, Σ') = RE(W, d, Σ)`." The trailing sentence then re-derives the same fact as an instance of RE-CWP, a result not stated until the *next* subsection. It adds nothing the direct argument hasn't supplied and forces the reader to reconcile two justifications for one fact, the second a forward pointer. This is exactly the "two paragraphs say the same thing" + forward-reference pattern.
**Required**: Delete the RE-CWP-instance sentence (the direct argument is complete), or relocate the cross-link into the RE-CWP subsection.

### Issue 2: Editorial defense of a result's status in RE-UDIST-∩
**ASN-0131, "Composing regions" section**: "this touch-implication is the *exact* — necessary and sufficient — characterisation of intersection-equality: settled, not for want of a sharper condition but because it *is* the condition."
**Problem**: The necessary-and-sufficient characterization is fully earned by the preceding paragraphs (⊆ unconditional; ⊇ refuted under both a non-injective and an injective arrangement; ⊆-half-plus-failure yields the iff). The clause "settled, not for want of a sharper condition but because it *is* the condition" is anticipatory rebuttal of an imagined "why not sharper?" objection — defensive meta-prose, not argument. (The adjacent "What it is not is *structural* …" sentence is load-bearing — it motivates Open Question 4 — and should stay.)
**Required**: Drop the "settled, not for want of a sharper condition but because it *is* the condition" clause.

### Issue 3: Notation reconciliation produces a mismatch it claims to resolve
**ASN-0131, "Fresh emissions and the addressable population" section**: "We keep ASN-0086's inherited name `L_R` (its subscript is that retraction type `Θ`) and render ASN-0086's emit operation `Emit_R` as `Emit_Θ` to match."
**Problem**: The sentence renames `Emit_R → Emit_Θ` "to match" but *keeps* `L_R`, leaving the slice on subscript `R` and the emit on subscript `Θ` for the same retraction type — a mismatch, not a match, that the reader must carry (the note even has to gloss "its subscript is that retraction type `Θ`"). This is notation housekeeping that adds friction rather than removing it.
**Required**: Standardize the subscript — either `L_Θ`/`Emit_Θ` throughout or `L_R`/`Emit_R` throughout — and drop the reconciliation gloss.

### Issue 4: Shift-based insert/delete paragraph — assumption-justification and non-monotonicity exposition around a one-line conclusion
**ASN-0131, "Stability" section, shift paragraph**: "ASN-0082 establishes this confinement only over its own modelling state: it models these primitives over a `(C, M)` state with no link, entity, or provenance store, and proves they write only `Σ.M(d)` and frame `Σ.C` …" and "the shift family is non-monotone *as a class*, and a single shift may make the fixed region's image *gain*, *lose*, or *both* …"
**Problem**: The load-bearing content of this paragraph is small: the M-only abstraction ("an arrangement edit confined to `Σ.M(d)`"), the named conservative-lift assumption, and the depth scoping (delete `#p = 2`, insert `#p ≥ 2`). Around it sit (a) a justification of *why* the assumption is needed — that ASN-0082's `(C, M)` model leaves `Σ.L`/`Σ.E`/`Σ.R` unconstrained — which is assumption-rationale prose, and (b) an exposition that the shift family is non-monotone "as a class," which merely re-states RE-EDIT's already-established global non-monotonicity. Both surround a conclusion the note itself reduces to "acts exactly as every ASN-0047 atomic mover above does."
**Required**: State the M-only principle once, attach the named conservative-lift assumption and the depth scoping, and cite the M-only conclusion already drawn for the K.μ movers; cut the (C,M)-model rationale and the shift-non-monotonicity exposition to a clause.

## OUT_OF_SCOPE

The seven Open Questions correctly defer their topics (whole-vs-touching-spans extent, endset multiplicity, V-rendering of unarranged content, a structural sufficient condition for intersection-equality, cross-store completeness, type-slot matches against content, link-subspace regions). No new OUT_OF_SCOPE items — and no out-of-scope operations are defined in the body (FINDLINKSFROMTOTHREE and FINDNUMOFLINKSFROMTOTHREE appear only as named contrasts, not as numbered cross-references or claims).

VERDICT: REVISE
