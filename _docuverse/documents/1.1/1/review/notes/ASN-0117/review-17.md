# Review of ASN-0117

## REVISE

### Issue 1: Coverage-invariance cited as single-step LP3 for a multi-step composite

**ASN-0117, "What shifts" / P4 (LinkSurvival)**: "every endset's *coverage* is unchanged (**LP3 (CoverageInvariance)**, ASN-0098)" and P4: "`coverage_{Σ'}(e) = coverage_{Σ}(e)` (DEL-LIMM + LP3)".

**Problem**: In the general (`R ≠ ∅`) case DELETE is defined as a *two-step* K.μ⁻ + K.μ⁺ composite, so `Σ → Σ'` is not a single transition. LP3 (CoverageInvariance) is the single-step lemma; coverage invariance across a composite is LP3★ (MultiStepCoverageInvariance), the closure of LP3. ASN-0098 supplies both, and the bridge is trivial — but the cited lemma does not literally apply to the composite as written.

**Required**: Cite LP3★ (or LP3 applied stepwise + the Closure schema) for the composite DELETE; LP3 alone suffices only for the `R = ∅` single-step realisation.

### Issue 2: Use-site inventory justifying the composite realisation

**ASN-0117, Effect (Case `R ≠ ∅`)**: "no single atomic transition expresses that: K.μ⁻ leaves survivors unshifted, K.μ~ preserves domain cardinality, K.μ⁺ adds content."

**Problem**: This is an inventory of what each *other* atomic transition does, used to justify the choice of a composite rather than to advance DELETE's definition. The carrier (the K.μ⁻ + K.μ⁺ decomposition) is already stated explicitly in the same paragraph; the enumeration of why the alternatives fail is meta-prose about the realisation choice, the kind of accretion the anti-bloat classifier targets.

**Required**: State that DELETE is the K.μ⁻ + K.μ⁺ composite (and the lone K.μ⁻ when `R = ∅`) and proceed; drop the per-transition inventory.

### Issue 3: Binding-versus-being motif restated across three sections

**ASN-0117, intro / "A span, not a position: binding versus being" / "What we have established"**: the binding-vs-being theme appears in the introduction ("keeping those two layers from contaminating each other"), as a dedicated section, and again in the conclusion ("the seam between binding and being … DELETE severs the first while the second remains untouched").

**Problem**: The dedicated section's core formal content is exactly DEL-REMOVE (arrangement ceases to bind) and DEL-CIMM/P0 (content does not cease to exist), already established. Its middle paragraphs re-narrate those two clauses interpretively and the motif then recurs verbatim-in-spirit in the conclusion. This is the "two paragraphs say the same thing in different words" pattern spread across the document.

**Required**: Keep one statement of the span-has-extent / position-binds-nothing distinction (it answers a consultation question and is worth one place), and remove the restatements of DEL-REMOVE/DEL-CIMM dressed as prose in the intro and conclusion.

## OUT_OF_SCOPE

### Topic 1: Lower-boundary well-formedness (span beginning before the first arranged position)
**Why out of scope**: The precondition already requires `p ∈ V_S(d)` with `J ≥ 1`, so the operation as specified never deletes below the origin; the note correctly defers the relaxed-boundary question to its Open Questions rather than treating it here.

### Topic 2: Reconstructibility / historical backtrack from the permanent store
**Why out of scope**: P0 guarantees the deleted bytes survive, but exact reconstruction of a prior arrangement is downstream machinery (backtrack), correctly listed as an open question, not an obligation of DELETE.

VERDICT: REVISE
