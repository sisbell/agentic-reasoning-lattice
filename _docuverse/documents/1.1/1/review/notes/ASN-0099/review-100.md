# Review of ASN-0099

## REVISE

### Issue 1: Duplicated K.μ~/A1a transitivity statement (forward-reference accretion)
**ASN-0099, "Link-Store-Inert Preservation" preamble and A1a body**:

Preamble: "The named reordering K.μ~ is the K.μ⁻ + K.μ⁺ composite, so A1a applies to it by transitivity."

A1a body: "The composite K.μ~ (the non-atomic K.μ⁻ + K.μ⁺ composite) preserves Σ.L by transitive composition of A1a at its two atomic constituents."

**Problem**: The same conclusion — "K.μ~ is the K.μ⁻+K.μ⁺ composite, so preservation applies transitively" — is stated twice. The preamble version is worse: it forward-references A1a *before A1a is stated* and pre-announces A1a's own conclusion. This is precisely the forward-reference meta-prose pattern (a paragraph pre-stating a downstream lemma's content). The reader meets the claim, then meets it again as the lemma's actual body.

**Required**: Drop the preamble's "so A1a applies to it by transitivity" clause. The preamble need only define `V ≡ V_atomic ∪ {K.μ~}`; the transitive-composition justification belongs solely in A1a's body, where it is properly stated.

### Issue 2: "F2 and F3 hold vacuously" mischaracterizes F3
**ASN-0099, "The Empty Query"**: "When `dom(Σ.L) = ∅` (the initial state, before the first K.λ), every query produces `∅`. F2 and F3 hold vacuously..."

**Problem**: F2 (`findlinks ⊆ result` = `∅ ⊆ result`) is vacuously/trivially true. F3 (`result ⊆ findlinks` = `result ⊆ ∅`) is *not* vacuous — it is a determinate constraint forcing `result = ∅`. Lumping both under "vacuously" misstates what F3 does in the empty-store case (it pins the implementation output to `∅`, which is the substantive content here).

**Required**: Separate the two: F2 holds vacuously; F3 forces `result(I, Σ) = ∅`.

## OUT_OF_SCOPE

### Topic 1: Combined filtered-and-scoped operation
The ASN correctly defers `findlinks_filtered_scoped(C, S, Σ)` to future work in "What We Have Not Specified." No action needed — flagged only to confirm it is appropriately scoped out.

### Topic 2: FOLLOWLINK / RETRIEVEENDSETS (inverse direction)
Resolving result endsets back to V-positions is correctly named as a separate operation. Not an error here.

VERDICT: REVISE
