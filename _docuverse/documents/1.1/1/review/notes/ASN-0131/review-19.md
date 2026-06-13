# Review of ASN-0131

This is a mature, careful note. I verified the load-bearing formal content and it holds: the worked instance computes correctly (the `e₃ ∩ dom(Σ.C) = ∅` field-agreement argument is sound; the half-open `[a₂, a₄)` span gives `{a₂,a₃} ⊆ coverage(e₁)` as claimed); RE-UDIST's factoring through the region-independent `Avail(Σ)` is valid and the image-over-union step is unconditional; RE-CWP's weakest precondition reduces correctly (`Δ`-touch ⟹ `I_R`-touch, with the `R=∅` collapse to `RE=∅`) and is genuinely finer than D-CWP's per-link form; the RE-RET backward direction is unconditional via R-Scope/R0a and the forward direction's hypothesis is correctly isolated. Two issues remain.

## REVISE

### Issue 1: K.λ emission is named as answer-moving but never derived
**ASN-0131, claims table RE-EDIT / stability section**: RE-EDIT asserts an exhaustiveness boundary — "only the content-subspace edits to `d` … and `K.λ` … can move the answer; every other transition leaves it fixed" — and characterizes the K.λ mover as "(emission may add a pair, retraction removes — RE-RET)."

**Problem**: The stability body derives the K.λ *retraction* sub-case at length ("**Under retraction.**", several paragraphs) but never the generic *emission* sub-case. The closing summary is likewise one-sided: it "respects the *active population* (a withdrawn link vanishing from it…)" — the population *shrinking* is treated, the population *growing* is not. The emission direction is not the throwaway monotone-add it might appear: a freshly emitted `ℓ_new` is answer-moving only if it is *addressable* in `Σ'`, and that rests on exactly the discipline + R0a (flat-antichain) argument the note already deploys to show the retraction emitter `b` is addressable. An exhaustiveness claim that names K.λ as a mover must substantiate both of its sub-cases.

**Required**: Add the one-clause derivation (or cite it): a generic K.λ emits fresh `ℓ_new ∈ dom(Σ'.L)`, addressable in `Σ'` by the same discipline/R0a reasoning used for `b`, with frame `M' = M` holding the image fixed; if some `Σ.L(ℓ_new).eᵢ` satisfies `touch_W`, the pair `(i, eᵢ)` is added (monotone), else the answer is unchanged. This is the population-grow analogue of E-MONO/F-LAMBDA (ASN-0127) and completes the K.λ side of RE-EDIT's boundary.

### Issue 2: Speculative downstream-layer mechanics in the retraction Θ discussion
**ASN-0131, "Under retraction" (the `Θ` paragraph)**: "it is a property the retraction layer (ASN-0086) must *furnish* — e.g. by confining `Θ`'s spans to the `s_R`-subtree (where unit depth, or any span with `s ≼ t` throughout, makes `s_R`-seating suffice) — the placement being that layer's mechanics, not ours to impose here."

**Problem**: This carries the `review-mode.anti-bloat` pattern. RE-0131 needs three things from this paragraph and gets them elsewhere: state the conditional `coverage(Θ) ∩ dom(Σ.C) = ∅`, flag that this ASN does not establish it, and route the exception to Open Question 6. The "*e.g.* by confining `Θ`'s spans to the `s_R`-subtree … makes `s_R`-seating suffice" clause is a sketch of *how ASN-0086 could discharge the hypothesis* — design speculation about a different layer, explicitly "not ours to impose here." It does not advance any claim of this note; achievability of the hypothesis is ASN-0086's concern, not ASN-0131's.

**Required**: Drop the `s_R`-seating "e.g." parenthetical and the "must furnish … placement being that layer's mechanics" elaboration; state the dependency as a bare conditional plus the OQ6 pointer. **Keep** the immediately preceding wide-span observation ("a *wide* type span … whose members need not satisfy `s ≼ t`") — that *is* load-bearing, since it is what shows the unit-depth field-agreement argument does not transfer and hence why the forward direction *must* be conditional rather than discharged here.

## OUT_OF_SCOPE

### Topic 1: Link-pairing and identity recovery
**Why out of scope**: RE-UNIT's deliberate withholding of link identity means a surfaced from-endset cannot be paired with its link's to-endset, and multiplicity is not recoverable. The note is right to route these to FINDLINKSFROMTOTHREE / counting / READLINK rather than claim them here; no drift.

### Topic 2: Multi-store and link-subspace-region completeness
**Why out of scope**: The non-co-resident link-store completeness question (Open Question 5) and the link-subspace-`W` case (Open Question 7) are correctly deferred — both belong to replication/BEBE and a sibling operation, not to this content-region query. No coverage gap to flag.

VERDICT: REVISE
