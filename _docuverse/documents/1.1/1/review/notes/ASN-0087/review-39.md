# Review of ASN-0087

## REVISE

### Issue 1: Reconciliation prose in "What Is Indexed?" is reviser drift
**ASN-0087, What Is Indexed?**: "The two statements are compatible: the LP12-definitional symmetry holds throughout and the content-reach route is symmetric, while the reflexive route is the home document's alone... This reconciles the unqualified-sounding 'no privileged position' with Case 2's 'available to the home document alone.'"
**Problem**: This paragraph reconciles the document's own wording rather than advancing reasoning. The phrase "This reconciles the unqualified-sounding X with Case 2's Y" is meta-commentary accreted to defend against a prior contradiction finding. The substantive content — the home document alone gains a reflexive route because MAKELINK places `ℓ` only in its arrangement — is real but buried under reconciliation scaffolding.
**Required**: Reduce to the substantive claim in one or two sentences (home document alone gets a reflexive route; content-reach route is symmetric). Delete the "the two statements are compatible / this reconciles" framing.

### Issue 2: Protocol-concurrency reasoning embedded in Inputs
**ASN-0087, Inputs (Reflexive authoring and prediction)**: "The prediction is *sound* only when no intervening `A_L(d)` emission occurs between authoring and execution: any intervening K.λ on `d` advances the frontier, so the predicted `ℓ` would no longer be the emission MAKELINK commits..."
**Problem**: That `ℓ` is deterministically derivable (and thus predictable, enabling reflexive endsets) is substantive and belongs here. But the soundness-under-intervening-emission caveat is a concurrency/protocol concern — the same territory the Atomicity section explicitly assigns to the protocol layer. It is protocol rationale sitting in a structural input slot.
**Required**: Keep the predictability statement; move or drop the intervening-emission soundness caveat (it is a protocol-layer concern, consistent with the deferral in *Atomicity*).

### Issue 3: D-SEQ★ verification ignores MAKELINK's own depth commitment
**ASN-0087, Invariant Preservation (D-SEQ★)**: "If `n_L = 0`, the K.μ⁺_L positioning rule gives `v_ℓ = [s_L, 1, ..., 1]` of the chosen depth `m ≥ 2`..."
**Problem**: M-DepthConv and the Effect section commit MAKELINK to the minimal depth `m = 2` for every first link it places (`v_ℓ = [s_L, 1]`). The D-SEQ★ verification instead reasons generically over "chosen depth `m ≥ 2`," contradicting the operation's own stated commitment. Not a logical error (the conclusion holds for any `m`), but the operation's invariant proof should apply the depth it actually fixes.
**Required**: State the empty-case `v_ℓ = [s_L, 1]` at depth 2 per M-DepthConv, fixing `m_L(d') = 2`; drop the generic "chosen `m ≥ 2`."

### Issue 4: Open Question already answered in the body
**ASN-0087, Open Questions**: "What abstract guarantee distinguishes a 'properly created' link visible in its home document's arrangement from a link allocated but not placed?"
**Problem**: The *Atomicity* section already characterizes this distinction concretely — `Σ_mid` (allocated, `ℓ ∉ ran(M(d))`, reflexive route unavailable) versus `Σ'` (placed, `v_ℓ ↦ ℓ`), captured by M-CompAtomicity. Listing it as open is internally inconsistent and adds noise.
**Required**: Remove the question, or rephrase to the genuinely open residue (e.g., what protocol-level guarantee should bound the visibility of `Σ_mid`).

## OUT_OF_SCOPE

### Topic 1: Well-formedness constraints on forward-reaching endset spans
**Why out of scope**: The remaining Open Questions about constraints on spans referencing not-yet-allocated addresses (beyond L4 generality and StandardAuthoring discipline) are genuine future territory, not errors in this ASN. They are correctly parked.

VERDICT: REVISE
