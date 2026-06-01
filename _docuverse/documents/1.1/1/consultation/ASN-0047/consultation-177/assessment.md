# Channel Assignment — ASN-0047 review-177

**Date:** 2026-05-31 22:10

## Issue 1: FrontierEquivalence presupposes every non-node entity is a tracked-allocator emission, with no backing invariant
Reason: Derivable from the ASN alone — K.δ is the only transition adding to E, and every non-node entity enters via an `inc(t,k)` step that places it on a tracked sub-allocator chain; the fix is to name this as a per-state invariant (or cite the K.δ discharge) so the lemma's "A exists" precedes "A is unique by T10a.6." No design-intent or implementation evidence required.

## Issue 2: K.δ's "M untouched / registration via E" claim is stated three times
Reason: Pure editorial deduplication internal to the ASN — collapse the three restatements into the normative Frame line.

## Issue 3: FrontierEquivalence is re-derived at three sites
Reason: Internal editorial fix — replace the two downstream re-derivations with a citation of the lemma's name and conclusion.

## Issue 4: Reviser-drift — K.δ k=1 paragraph reasons about a case its own dispatch excludes
Reason: Internal editorial deletion — the per-`(t,1)` uniqueness sentence already closes the case; no external input needed.

## Issue 5: Multiple sections defer the same obligations to ExtendedReachableStateInvariants / the K.μ~ fixity proof
Reason: Internal restructuring — give each derivation (P4a, S8★) once and cite by label elsewhere; no design or implementation question is at stake.

## Issue 6: The override is announced with meta-prose about not restating it
Reason: Internal editorial deletion — retain the identity `d ∈ dom(M) ⟺ d ∈ E_doc` and translation rule, drop the self-referential framing.
