# Review of ASN-0047

I checked the elementary transitions, the coupling/composite machinery, the K.μ~ decomposition, and the per-state/composite-boundary verification. The mathematics is, as far as I can verify, sound and unusually complete — boundary cases (empty document via full K.μ⁻ clearance, first insertion via ValidFirstInsertionPosition, interior replacement via suffix-rebuild, orphan links, cross-subspace transposition exclusion) are all genuinely handled. The findings below are precision and accreted meta-prose, the latter explicitly within this note's `review-mode.anti-bloat` mandate.

## REVISE

### Issue 1: Navigational essay in a structural slot (K.δ discharge section)
**ASN-0047, "K.δ case (ii) discharge and parent-allocator activation"**: "Each non-node K.δ event's freshness conjunct is discharged by the per-k mechanism stated in the K.δ definition... this section does not re-walk that regime. What follows is the parent-allocator-activation material the definition does not contain."
**Problem**: The opening paragraph describes the section's relationship to the K.δ definition rather than advancing any claim. This is essay content in a structural slot — the reader must skip it to reach the per-k activation table. It matches the flagged pattern "new prose explaining the document's division of labor rather than the object-level content."
**Required**: Delete the preamble and open with the substantive per-k parent-allocator activation. The table already carries the content.

### Issue 2: J1★/J1'★ deferred forward from multiple sections
**ASN-0047, "Permanence" / "Coupling and isolation" / "Scoped coupling constraints"**: The provenance couplings are gestured at in *Permanence* ("Arrangements admit three modes..."), introduced in *Coupling and isolation* ("The provenance couplings J1★... are content-subspace–scoped"), and only derived in *Scoped coupling constraints*. Each earlier mention defers downstream.
**Problem**: This is the flagged pattern "multiple paragraphs in different sections defer to the same downstream location." The repeated "these are content-subspace–scoped, see below" advances nothing until the wp derivation.
**Required**: State the couplings once, at the derivation site; replace the earlier mentions with at most a single pointer, or drop them.

### Issue 3: Over-claim in the three-step replacement example
**ASN-0047, "Worked example: prior-provenance and first-time-transcluded replacements"**: "(The foreign origin is what makes `(aₓ, d) ∉ R` reachable: a `d`-origin address arranged in `d` would, by J0/J1★ coupling, immediately yield `(aₓ, d) ∈ R`.)"
**Problem**: Foreign origin is sufficient but not necessary for `(aₓ, d) ∉ R`. A `d`-origin address allocated by K.α and transcluded by K.μ⁺ only into some `d' ≠ d` (K.μ⁺ permits `origin(a) ≠ d'`) is never arranged in `d`, so `(aₓ, d) ∉ R` while `aₓ ∈ dom(C)`. The discriminator is *arranged-in-`d`*, not origin. As written, "is what makes...reachable" misstates the reachability condition.
**Required**: Weaken to "foreign origin is one way to obtain `(aₓ, d) ∉ R`," or state that the discriminator is whether `aₓ` was ever arranged in `d`, independent of origin.

## OUT_OF_SCOPE

### Topic 1: Concurrency of same-document allocation
The Open Questions raise serialization of link allocation under concurrent operations. This is genuinely new territory (concurrency model), correctly deferred rather than treated here.

VERDICT: REVISE
