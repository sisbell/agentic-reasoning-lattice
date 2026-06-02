# Channel Assignment — ASN-0086 review-241

**Date:** 2026-06-01 21:23

## Issue 1: Nullify's *Rationale* contradicts the self-emit branch of its own precondition P-tgt
Reason: The Rationale grounds the operation in both Nelson's design intent and the udanax-green exact-match guard, so reconciling it requires knowing whether retraction was *meant* to be scoped to pre-existing owned material and whether the implementation actually forbids retracting an unbaptized address — neither is settled by the ASN.
Nelson question: Was retraction intended to apply only to already-existing, owned addresses, or does a baptize-and-retract-in-one-atomic-step (target owned at commit) fall within the "only the owner may withdraw" intent?
Gregory question: Does the granfilade exact-match guard (`tumblereq`, `granf2.c:37`) require a retraction's target address to already reside in the link store, or can a single operation allocate and retract a fresh address in one step?

## Issue 2: The K.λ L3-discharge argument is stated three times in near-identical words
Reason: Purely an internal deduplication of prose the note already contains; consolidating the L3-discharge to one site and citing it is derivable from the ASN alone.

## Issue 3: R0's freshness proof re-derives ASN-0093 freshness lemmas instead of citing them
Reason: The fix replaces a hand re-derivation with citations to FirstEmissionFreshness/SubsequentEmissionFreshness — lemmas the note already builds on and cites in its own worked sketch for exactly this `dom(C) ∪ dom(L)` exclusion, so it is internal.
