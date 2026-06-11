# Channel Assignment — ASN-0121 review-33

**Date:** 2026-06-11 15:02

## Issue 1: Σ overloaded as both system state and span-set sequence
Reason: Purely notational — the fix is choosing a fresh metavariable for ASN-0053's span-set sequence, and the collision plus its resolution are fully visible in the ASN's own text. Neither design intent nor implementation evidence bears on a symbol rename.

## Issue 2: FL-WP case (a)'s wp is displayed as a post-state predicate
Reason: The pre-state unfolding (`ℓ ∉ nullified(Σ') ≡ ¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))`) is already derived in the ASN's own prose immediately after the display; the fix is moving it into the displayed formula. Internal.

## Issue 3: FL-WP case (a) writes the link value as a 3-tuple while reasoning about arity N > 3
Reason: The arity-N reasoning and the L3 license for higher arity are already present and correct in the ASN; only the displayed tuple notation must be generalized to exhibit N slots. Internal.

## Issue 4: nullified-monotonicity is established three times, and the first attribution overreaches R6a
Reason: The canonical composite derivation (F-PRES constancy on non-K.λ steps plus R6a across K.λ) already exists at the second site; the fix is consolidating to it, forward-pointing the first mention, and citing it from FL-RET. R6a's correct narrower scope is already identified, so no external consultation is needed.

## Issue 5: meta-prose accretion around the WP scope paragraph, FL-SND, and FL-JUNK
Reason: Pure deletion/compression — reduce the precedent inventory to a bare citation, drop the structural-justification sentence, and remove FL-JUNK's redundant hypothesis clause whose content the proof's existing L12 citation already carries. Internal.
