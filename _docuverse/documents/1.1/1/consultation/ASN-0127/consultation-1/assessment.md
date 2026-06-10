# Channel Assignment — ASN-0127 review-1

**Date:** 2026-06-09 23:34

## Issue 1: F-ADD carries a spurious disjointness precondition and mislabels the property
Reason: Pure set-algebra: unfold F-MATCH (present in the ASN), then apply ∩/∪ distribution and existential-over-disjunction. The review already supplies the complete derivation; no design intent or implementation evidence is at stake.

## Issue 2: The worked illustration uses links that violate L3
Reason: L3's structure (n ≥ 3, non-empty slot-3 type endset) is an already-established invariant restated/cited in the note, L4 (endsets may reference any address in T) is in the ASN, and the match re-verification runs entirely on F-MATCH — so constructing a valid three-endset example and recomputing is internal.

## Issue 3: The worked illustration's K.μ⁻ step misstates contraction semantics
Reason: The prefix-retention semantics of K.μ⁻ (D-SEQ★, ASN-0047) is an established named result the review has already identified, and the corrected example is a mechanical restatement using F-IMG; nothing about intent or implementation is unsettled.

## Issue 4: F-IMG-MONO, F-IMG-CONTR, F-IMG-SWING are asserted without derivation
Reason: The missing proofs follow from the established K.μ⁺/K.μ⁻/K.μ~ frame conditions and K.μ~-FIX, which the review spells out in full; writing the short derivations is internal formal work requiring no new evidence or intent.

## Issue 5: E-CONS asserts an "exactly" characterization without showing the exclusion direction
Reason: The exclusion direction just chains E-INV — already stated in the note's existence-anchoring section — with a two-case split that the review provides verbatim, so the fix is fully internal.
