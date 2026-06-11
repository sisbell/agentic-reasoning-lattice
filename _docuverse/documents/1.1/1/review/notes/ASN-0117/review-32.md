# Review of ASN-0117

The ASN is in good shape technically — the citation-stub strategy works, the two-realisation split (K.μ⁻+K.μ⁺ vs. lone K.μ⁻) is correctly drawn at `R = ∅`, the range identity `ran(M'(d)) = ran(M(d)) \ A_del^{excl}` checks out including the cross-subspace disjointness step, and the worked examples cover the genuine boundaries (leading-span, suffix, delete-everything, within-document sharing, transclusion). The remaining issues are a precondition that is weaker than the discharge it must support, two citation-discipline gaps, and accumulated meta-prose.

## REVISE

### Issue 1: Reachability precondition is too weak for the composite-boundary discharge
**ASN-0117, DELETE Precondition / Effect**: "`Σ` is `→*`-reachable from the initial state `Σ₀` (so the per-state invariant package of ExtendedReachableStateInvariants, ASN-0047, holds at `Σ`)" … "DELETE is a valid composite from a `→*`-reachable pre-state, so its post-state is a composite boundary of a valid trace, and the three composite-boundary properties — P4★, P4a, P7a — hold there directly."
**Problem**: ExtendedReachableStateInvariants licenses the per-state package only for states reachable *by elementary transitions drawn from valid composites*, and the composite-boundary properties only *at composite boundaries*. Bare `→*`-reachability (the SequentialTransitionAxiom closure) admits elementary sequences not drawn from valid composites — in particular, states strictly inside another composite. From such a Σ: (i) the parenthetical claim that the per-state package holds is not licensed by the cited theorem; (ii) appending DELETE does not extend a *valid* transition trace, so the post-state is not a boundary of a valid trace, and the P4a discharge — which quantifies over valid traces to the post-state — does not go through.
**Required**: Strengthen the precondition to "Σ is a composite boundary of a valid transition trace from Σ₀" (P4a's sense, ASN-0047), and have both the per-state-package claim and the P4★/P4a/P7a discharge cite that hypothesis.

### Issue 2: J1★ discharge silently narrowed to the operated document
**ASN-0117, Effect (coupling discharge)**: "**J1★** (every I-address *new to* `d`'s content-subspace range must be recorded in `R`) holds because DELETE introduces *no* range-new content: every survivor's I-address that the K.μ⁺ step re-places was already in the content-subspace range of `M(d)` at its old position…"
**Problem**: ASN-0047's J1★ quantifies over *every* `d ∈ E'_doc`, not just the operated document; the parenthetical restatement bakes the narrowing into the obligation itself. For `d' ≠ d` the discharge is immediate — DEL-FDOC gives `M'(d') = M(d')`, so no address is range-new for any other document — but that step is never stated. (J1'★ and J0 are fine as written: their antecedents `R' ∖ R = ∅` and `dom(C') ∖ dom(C) = ∅` empty the quantifier over all documents at once.)
**Required**: State J1★ at its actual quantification and add the one-line `d' ≠ d` discharge via DEL-FDOC.

### Issue 3: DEL-LIMM justified by restating its conclusion instead of citing its premises
**ASN-0117, Frame, DEL-LIMM**: "DELETE allocates no link and edits none, so `dom(L)` neither grows nor shrinks."
**Problem**: This paraphrases the frame clause rather than deriving it. The premises are one citation away: ASN-0047's K.μ⁻ (per-subspace scope) adds the frame clause `L' = L`, the amended K.μ⁺ frame lists `L' = L`, and J2 supplies `L' = L` outright for the `R = ∅` single-step realisation. DEL-FENT and DEL-FPROV name their component-frame premises; DEL-LIMM, alone among the frame clauses, does not.
**Required**: Derive DEL-LIMM by citation to the K.μ⁻/K.μ⁺ frame clauses (composite case) and J2 (single-step case), matching the discipline used for DEL-FENT/DEL-FPROV.

### Issue 4: Anti-bloat — the "we do not re-derive" disclaimer recurs five times, plus twin deferrals
**ASN-0117, throughout**: "we do not re-derive it: it is the foundation contraction of ASN-0082"; "We do not re-derive the post-contraction domain"; "We do not re-prove well-formedness either"; "we do not re-derive them. We name DELETE's clauses but derive them by citation"; "We do not re-derive it; we only refine the subset to the *exact* loss"; the defensive framing "This refinement of P4's subset is justified, not asserted:"; and DEL-FENT and DEL-FPROV both reading "by the composite-frame argument given in the Effect section above."
**Problem**: The citation discipline is the document's method, announced once per section in slightly different words — the same meta-statement restated, defending the method rather than advancing any claim. The "justified, not asserted" clause addresses the reviewer, not the reader; the content after its colon (the `dom(C)`/`dom(L)` disjointness step) is the substance and stands alone. DEL-FENT/DEL-FPROV deferring jointly to the same upstream paragraph is the multiple-deferral pattern.
**Required**: State the citation discipline once ("We name DELETE's clauses but derive them by citation" suffices); delete the remaining disclaimers and the "justified, not asserted" framing, keeping the citations and the substantive disjointness step; give the composite-frame discharge a single name and let DEL-FENT/DEL-FPROV cite it once.

## OUT_OF_SCOPE

### Topic 1: DELETE at common V-position depth m > 2
**Why out of scope**: The precondition fixes `m = #p = 2` because the foundation contraction (ASN-0082) is proven at depth 2 only. Extending the left-shift to deeper text subspaces (D-CTG-depth's shared-prefix reduction suggests it generalizes) is future foundation work, not an error in this ASN.

### Topic 2: Rejection semantics for non-contained spans
**Why out of scope**: DELETE is partial — the containment precondition excludes spans not wholly within the arranged run. What an implementation signals when handed such a span is interface territory for a future ASN, consistent with how REARRANGE_K's partiality is handled.

VERDICT: REVISE
