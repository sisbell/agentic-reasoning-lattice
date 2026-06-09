# Channel Assignment — ASN-0126 review-2

**Date:** 2026-06-08 20:51

## Issue 1: Single-source `|F| = 1` blocks ASN-0086's Nullify and contradicts the "rejects nothing" claim
Reason: Choosing between re-modeling retraction as an F=1 Unary marker vs. admitting a zero-source case hinges on whether unattributed (empty-source) retraction is a genuine design requirement and whether the implementation actually relies on it — design intent (Nelson) and implementation evidence (Gregory).
Nelson question: Is an *unattributed* retraction — one with no source/proposer recorded — an intended, essential capability of the retraction design, or may every retraction legitimately carry a single attributing source span?
Gregory question: In udanax-green, does the retraction/nullify operation ever create a link with an empty from-set, or does it always record a source address for the retracting party?

## Issue 2: `Sh-conf` is undefined for unregistered types — P4 is ill-defined for them
Reason: Pure formal gap internal to this note — add "K is registered" to `K.λ_sh`'s precondition and adjust P4. No design or implementation input needed.

## Issue 3: Registry keyed by raw endset vs. coverage class — conflicts with ASN-0086 TypeEquivalence
Reason: Reconciliation with ASN-0086's TypeEquivalence (`K ~ K'` by coverage) is derivable from corpus content already present; state that registration keys on the coverage class `[K]` and that `shape`/`idem`/`Sh-conf` respect `~`. Internal.

## Issue 4: ASN-0086 lemmas are imported into `→_sh` without establishing the reachability inclusion
Reason: One-line proof that `→_sh ⊆ →` (each `K.λ_sh` step is a `K.λ` step plus a precondition) hence `→_sh*`-reachable ⊆ `→*`-reachable; fully derivable from the note's own definition of `→_sh`. Internal.

## Issue 5: Cross-ASN reference by number to a non-foundation ASN
Reason: Editorial fix — replace "Retired ASN-0095's territory" with a descriptive phrase ("predicate-composition rules"). Internal.
