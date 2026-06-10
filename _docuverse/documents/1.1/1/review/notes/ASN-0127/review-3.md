# Review of ASN-0127

This is a careful, well-constructed note. The two-phase factoring is clean, F-CIL is a genuine keystone, the F-IMG-SWING witness is worked in full, and E-CONS is correctly proved in both directions. The findings below are narrow.

## REVISE

### Issue 1: D-NONMONO's K.μ⁻ inclusion drops the Σ.L-preservation step

**ASN-0127, "Discovery anchoring" → D-NONMONO, K.μ⁻ bullet**: "the arrangement contracts, so `image(W, d_q, Σ') ⊆ image(W, d_q, Σ)` (F-IMG-CONTR); the resolved request can only shrink, and since findlinks is monotone in its I-argument (F-IMONO), the discovery set can only shrink with it: `findlinks_disc(W, d_q, Σ') ⊆ findlinks_disc(W, d_q, Σ)`."

**Problem**: F-IMONO is a *single-state* law — `I' ⊆ I ⟹ findlinks(I', Σ) ⊆ findlinks(I, Σ)`, both sides at the same `Σ`. The conclusion compares two *different states*:

> `findlinks(image(W,d_q,Σ'), Σ') ⊆ findlinks(image(W,d_q,Σ), Σ)`.

F-IMG-CONTR supplies `image(W,d_q,Σ') ⊆ image(W,d_q,Σ)`, but F-IMONO alone cannot cross the `Σ' → Σ` change in the comprehension's evaluation state. Applying F-IMONO at `Σ'` gives `findlinks(image', Σ') ⊆ findlinks(image, Σ')` — whose right side is the *old* image at the *new* state, not `findlinks_disc(W,d_q,Σ)`. The missing premise is exactly the note's central observation: K.μ⁻ moves `Σ.M`, not `Σ.L`. That premise (F-PRES → F-INERT) is what lets the comprehension state be held fixed. Its omission is conspicuous precisely because the note is otherwise meticulous about which state component each transition touches — and this is the one clause that makes a clean directional `⊆` claim depending on it. (The same uncited transfer silently underlies the "can add new link matches" and "may rise or fall" transfers in the K.μ⁺ and K.μ~ bullets; it only becomes load-bearing for the K.μ⁻ inclusion.)

**Required**: Cite F-PRES/F-INERT to bridge the states, e.g.: "K.μ⁻ preserves `Σ.L` (F-PRES), so `findlinks(·, Σ') = findlinks(·, Σ)` (F-INERT); hence `findlinks_disc(W,d_q,Σ') = findlinks(image(W,d_q,Σ'), Σ) ⊆ findlinks(image(W,d_q,Σ), Σ) = findlinks_disc(W,d_q,Σ)` by F-IMONO at `Σ`."

### Issue 2: Worked illustration misattributes the existence-invariance citation

**ASN-0127, "Worked illustration", final line**: "But `findlinks({a₁, a₂}, Σ') = {L₁, L₂}` (existence non-zero — the links persist in the store, their coverage unchanged by D-NONMONO and F-PRES)."

**Problem**: D-NONMONO is the *non-monotonicity* result for `findlinks_disc`; it establishes nothing about coverage invariance, and citing it to justify an *invariance* (`findlinks({a₁,a₂},Σ') = {a₁,a₂}`-fixed result unchanged) points at the opposite phenomenon. The fact carrying this line is that K.μ⁻ preserves `Σ.L`, so the fixed-`I` comprehension is invariant — that is F-INERT (and per-link coverage invariance is E-INV / LP3★). D-NONMONO does not belong in this citation.

**Required**: Replace "by D-NONMONO and F-PRES" with F-INERT (K.μ⁻ preserves `Σ.L`, so `findlinks({a₁,a₂},·)` is unchanged), optionally noting E-INV for the per-link coverage permanence.

### Issue 3: `V_atomic` is used before it is bound

**ASN-0127, F-PRES**: "Every transition in `V_atomic ∖ {K.λ} = {K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}` ..."

**Problem**: The symbol `V_atomic` first appears here, but "State and notation" introduces the operations under the name "The K-transition vocabulary" and never binds `V_atomic`. The reader can back out `V_atomic` from the displayed set difference, but in a note this precise about notation the symbol should be defined at introduction rather than inferred at first use.

**Required**: In "State and notation," name the atomic vocabulary explicitly — `V_atomic = {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}` (ASN-0047), with K.μ~ the named composite — so F-PRES/F-INERT reference a bound symbol.

## OUT_OF_SCOPE

### Topic 1: Uniform per-slot treatment in F-MATCH (type-slot matching)

`matches` ranges its existential over all slots including the type slot, so a query `I` containing a type address would match links by their classifier endset. The worked example sidesteps this (`a_θ ∉ I`), and the per-slot-universal vs per-link-existential question is already named in Open Question 2. Correctly deferred — not a defect in this note.

**Why out of scope**: The slot-semantics refinement is new territory the note explicitly flags for future work; the primitive's uniform existential is a stated design choice, not an error.

### Topic 2: `findlinks` over a full arrangement range vs ASN-0098's `discoverable_from`

`findlinks(ran(Σ.M(d)), Σ)` coincides with the set of links discoverable from `d` (LP12), so `findlinks_disc` is the region-restricted refinement of `discoverable_from`. Spelling out this bridge would aid the reader but is the subject of Open Question 4 (composition with ASN-0098).

**Why out of scope**: The composition with the LP** layer is named as future work; the note's self-containment does not require it.

VERDICT: REVISE
