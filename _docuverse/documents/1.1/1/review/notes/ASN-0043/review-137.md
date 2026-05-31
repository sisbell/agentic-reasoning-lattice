# Review of ASN-0043

## REVISE

### Issue 1: The Link definition's prose enumerates downstream consumers instead of advancing the definition, and misattributes the `.type` accessor

**ASN-0043, Definition — Link**: "with the third slot designated as the type endset for every arity N ≥ 3 — the slot-3-as-type designation being carried by L3 (which requires the type endset non-empty at every arity) and the Named accessor L8 (which fixes `.type ≡ .e₃`), of which the arity-3 case is the standard triple (StandardTriple, below)".

**Problem**: This is forward-reference accretion of exactly the kind this note is flagged for. The formal definition is `Link = {(e₁, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}` — it does **not** designate slot 3 as anything; "slot 3 is the type" is a naming convention imposed later by L3 (non-emptiness) and the Named accessor. The clause justifies the designation by inventorying its downstream carriers (L3, L8, StandardTriple) rather than advancing the definition's meaning. Worse, it is inaccurate: `.type ≡ .e₃` is introduced by the *Named accessor* paragraph under StandardTriple, not by L8 — L8 merely *uses* `.type`. The prose thus relocates a definition's origin to a downstream consumer (reviser drift).

**Required**: Reduce the Link definition to its formal content (an N-tuple of endsets, N ≥ 3). State the slot-3-as-type convention once, at the site where it is actually fixed (the Named accessor / StandardTriple), without the L3/L8/StandardTriple inventory and without attributing the accessor to L8.

### Issue 2: L5's formal statement is set-theoretic extensionality, not a model invariant; its load-bearing content is unformalized

**ASN-0043, L5 — EndsetSetSemantics**: "`Σ.L(a).eᵢ = Σ.L(a').eⱼ ⟺ (A (s, ℓ) :: (s, ℓ) ∈ Σ.L(a).eᵢ ⟺ (s, ℓ) ∈ Σ.L(a').eⱼ)`".

**Problem**: Since `Endset = 𝒫_fin(Span)`, endsets are sets, and this biconditional is the axiom of extensionality — true of all sets, asserting nothing specific to the link model. The substantive claim L5 intends — *order carries no meaning and the model exposes no positional accessor within an endset* — is a statement about the operators the model provides, and it lives only in the prose ("(ii) no operator in the model selects a span by position"). As written, the INV labelled "EndsetSetSemantics" formalizes a tautology while leaving its actual content informal. The dual L6 (SlotDistinction) does carry real content (a positional accessor *across* slots), which makes the asymmetry sharper: L5's formal half says nothing.

**Required**: Either drop the tautological biconditional and state L5 as the structural commitment it is (no span-positional accessor exists; equality of endsets is inherited from `𝒫_fin`), or give it genuine formal content. A model invariant should not reduce to extensionality.

## OUT_OF_SCOPE

None — the Open Questions already route transclusion/link-store consistency, coverage-equivalence for queries, and link/content allocation ordering to future ASNs, which is correct.

VERDICT: REVISE
