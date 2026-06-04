# Review of ASN-0099

## REVISE

### Issue 1: No weakest-precondition analysis; all dynamic results are forward-only
**ASN-0099, "Persistent Discoverability (I-Side)" / F11**: "The corresponding V-side claim — fixing `(R, d)` and quantifying across edits — is a theorem of neither F11's persistence nor F19's monotonicity below, and could not be: K.μ⁻ can shrink `ran(Σ.M(d))`, so a V-position discoverable at `Σ` may be contracted out of the arrangement at `Σ'`."

**Problem**: Every dynamic characterization in the ASN is forward (strongest-postcondition style): F9 (inert preservation), F9-λ (the K.λ increment as `findlinks(I,Σ) ⊎ {ℓ_new}/∅`), F11 (I-side persistence), F19 (monotonicity). The ASN never computes a weakest precondition. The natural non-trivial case is handed to the reader by F11 itself: V-side discoverability `findlinks_V(R, d, ·)` is *not* preserved across arrangement edits, but the ASN stops at "could not be" without characterizing *which* edits preserve it. ASN-0098 supplies exactly the I-level tool (LP12a, `wp(K.μ⁻[d,R], discoverable_from(a, d, ·))`); ASN-0099 should compose it through `image` to give the V-side wp for its own operation. As written, the depth standard ("find a non-trivial wp case — e.g., wp for link discoverability is preserved") is unmet.

**Required**: Add a weakest-precondition claim for V-side discoverability of a fixed link under K.μ⁻ (and K.μ⁻+K.μ⁺), composing image with ASN-0098's LP12a — or justify explicitly why wp is not the appropriate framing for a read-only operation, beyond the single dismissive sentence in F11.

### Issue 2: State-tuple component ordering inconsistent with the foundation and internally
**ASN-0099, "Completeness"**: "states of the form `Σ = (C, L, M, E, R, …)`"; **"Link-Store-Inert Preservation"**: "ASN-0047's *extended* state `Σ = (C, L, M, E, R)`".

**Problem**: ASN-0047 (foundation) fixes the extended state as `Σ = (C, L, E, M, R)` (see Σ₀ and the ValidComposite★ definition). ASN-0099 uses `(C, L, M, E, R)` — `M` and `E` transposed — in two places, and additionally appends a trailing `…` in the Completeness instance, implying components ASN-0047 does not have. The set is the same and the components are named, so nothing is semantically broken, but a precise reader must reconcile three orderings.

**Required**: Use ASN-0047's `(C, L, E, M, R)` ordering verbatim and drop the trailing `…`.

## OUT_OF_SCOPE

### Topic 1: The reader-facing meaning of queries over I-addresses outside `dom(Σ.C) ∪ dom(Σ.L)`
**Why out of scope**: Correctly listed under "What We Have Not Specified." `matches` is well-defined for arbitrary `I ⊆ T` (coverage ∩ I), and `findlinks_V` only ever supplies store-resident I-sets via S3★, so there is no well-definedness gap here — only an interpretive question for a future ASN.

### Topic 2: Implementation auditability and K.λ-to-visibility latency bounds
**Why out of scope**: The two Open Questions concern an index/witness discipline and a timing guarantee. Both are genuinely new territory (implementation-conformance machinery, temporal semantics), not defects in this ASN's abstract specification.

VERDICT: REVISE
