# Review of ASN-0099

The mathematical content is strong: definitions are guarded with their load-bearing preconditions, the V-side/I-side factoring is clean, F9/A1a names each operation's frame clause rather than hand-waving "by the same reasoning," and the ASN correctly *declines* to claim V-side persistence (noting K.μ⁻ can contract a position out of `dom(M(d))`). The worked example exercises F1, F6, the filtered conjunction, cross-subspace imaging, and both F9 and F9-λ against concrete states. I checked the F4 individuation witnesses, the unfiltered-as-union-of-filtered recovery identity, F13's existential-over-disjunction step, and F9-λ's disjoint-union split — all sound.

The findings below are the anti-bloat patterns this review mode is tasked to surface.

## REVISE

### Issue 1: Foreshadowing meta-prose in a structural slot
**ASN-0099, "A Two-Phase Factoring" (closing sentence)**: "The two phases consult components with different stability properties — the mutable Σ.M and the monotonic Σ.L."
**Problem**: This sentence does not advance the factoring argument it terminates — `findlinks_V` is already fully defined by F12 at that point. It foreshadows the stability contrast that is developed substantively later (the monotonicity of `Σ.L` in Link-Store-Inert Preservation and F8/Determinism; the mutability of `Σ.M` in F11's note that K.μ⁻ shrinks `ran(Σ.M(d))`). It is non-advancing orienting prose duplicating downstream content.
**Required**: Delete the sentence; the stability distinction is earned where it is used.

### Issue 2: F5 "Derivation" restates the claim rather than deriving it
**ASN-0099, "Identity, Not Value", F5**: The statement already carries its own justification — "each decided by address-level membership in coverage(Σ.L(a).eᵢ), with no reference to content values" — and the appended "Derivation" re-enumerates the same consulted components ("consults only |Σ.L(a)|, per-slot endsets ... Σ.C does not appear") and repeats the distinct-α,β independence point.
**Problem**: Two passages in the same claim say the same thing in different words. The "Derivation" adds only the per-slot reduction `α ∈ coverage(eᵢ)`, which is already implied by the statement's "address-level membership."
**Required**: Either fold the one genuinely new step (per-slot membership reduction) into the statement and drop the redundant "Derivation" header, or strip the justification from the statement and let the Derivation carry it — not both.

## OUT_OF_SCOPE

None beyond what the ASN already lists in "What We Have Not Specified" (procedure, caching, replication, access control, FOLLOWLINK/RETRIEVEENDSETS), which are correctly deferred.

VERDICT: REVISE
