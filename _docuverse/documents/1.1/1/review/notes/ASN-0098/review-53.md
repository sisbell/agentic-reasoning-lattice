# Review of ASN-0098

## REVISE

### Issue 1: Achievability section is forward-reference accretion around the canonical construction
**ASN-0098, "Boundary and Width Behaviour" (Achievability paragraphs)**: "The tight case is reached by the canonical construction, instantiated concretely in the worked example below; the one fact that construction turns on but the example shows only by instance is that the emission-frontier bound `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)` is what discharges tightness..." and "Cross-chain interference is excluded by LP-Fin Corollary, which already establishes ... What remains, and is not implied by the corollary, is tightness against `A_X(d_0)`'s own *future* emissions: the corollary characterises interval membership but does not say which of those chain indices are allocated at `Σ_e`."
**Problem**: This is meta-prose about the argument rather than the argument. It defers forward to "the worked example below," narrates which fact "the example shows only by instance," and spends two sentences describing what the LP-Fin Corollary does *not* imply before supplying the actual content (the emission-frontier choice). A reader following the achievability claim must skip past the commentary to reach the one operative sentence (the frontier choice and its contiguous-segment consequence).
**Required**: Delete the "what is/isn't implied by the corollary" framing and the "the example shows only by instance" deferral. State directly: the emission-frontier bound `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)` confines candidate chain indices to `≤ m`, all of which are allocated at `Σ_e` by the contiguous-initial-segment property — which is exactly the surviving derivation that follows.

### Issue 2: LP12b carries a "consistent with — but not required for" parenthetical
**ASN-0098, LP12b**: "(StoreT4Validity additionally supplies that each `ℓ' ∈ dom(Σ.L)` is T4-valid, which is consistent with — but not required for — the chain-derived structural form to inhabit `F`.)"
**Problem**: The parenthetical introduces a fact and then immediately disclaims that the fact is used. Prose whose own content states it is "not required" advances no reasoning; it is exactly the residue the anti-bloat classifier targets.
**Required**: Delete the parenthetical. The three-step chain (ChainMembershipForOrigin → FirstEmission/ChainDiscipline → M0) already discharges `dom(Σ.L) ⊆ F` without it.

### Issue 3: F-validity proof closes with a defensive generality justification
**ASN-0098, "Boundary and Width Behaviour" (F-T4 paragraph)**: "This direct check covers registered and unregistered `d` uniformly, since it appeals only to the form `[d, 0, s, k]` and not to any active chain."
**Problem**: The preceding sentences already perform the clause-by-clause T4 check on the form `[d, 0, s, k]`. This closing sentence re-asserts that the check is form-only — a defensive justification of why the proof is general, not a step of the proof. It restates what the reader has just seen.
**Required**: Remove the sentence; the form-only check stands on its own.

### Issue 4: LP11 re-derives a foundation result rather than citing it
**ASN-0098, LP11**: "The second postcondition `ran(Σ'.M(d)) = ran(Σ.M(d))` is derived by taking images on both sides of the bijection equation. For every `v ∈ dom(Σ.M(d))`, the equation gives ..."
**Problem**: ASN-0047 (a foundation) already supplies range-invariance for K.μ~ — its J3 cites "K.μ~-RANGE (range-invariance)." A full re-derivation of `ran(Σ'.M(d)) = ran(Σ.M(d))` here duplicates an available foundation lemma. Foundations may be cited without restating.
**Required**: Replace the half-paragraph image-chase with a one-line appeal to ASN-0047's K.μ~-RANGE, retaining only the projection-specific consequence (`project' = π(project)`), which is the genuinely new content.

## OUT_OF_SCOPE

The Open Questions (reverse-discovery primitive, V-order of projected positions, link-to-link induced discovery, cross-document operation-sequence equivalence, fork-without-link-transclusion, link-canonical contraction) are correctly deferred — each names state/operations/invariants that belong to a successor ASN, not gaps in this one. No additional out-of-scope flags.

The core development (project as a live computation, LP4–LP11 operation effects, LP12/LP12a discoverability and wp, LP-Fin interval finitude, LP19/LP19a tightness, LP20/LP21) is sound: cases are covered, boundary cases (empty endset, empty arrangement, `R = ∅`, content-emptying retention) are handled explicitly, and the LP-Fin length-induction (sub-cases A/B with the `#d ≤ #d_0` bound and T4 endpoint exclusion of `#d = z_2`) is complete.

VERDICT: REVISE
