# Channel Assignment — ASN-0128 review-13

**Date:** 2026-06-11 02:45

## Issue 1: Emit_K under idem=⊥ has no home-validation semantics
Reason: Internal. The repair pattern already exists in the note — I1's validate-where-read home validation with rejection semantics, grounded in EmitAddress totality (ASN-0086) and the Gregory discipline already cited there. Under idem=⊥ every admitted call reads `d`, so the same principle yields uniform validation; stating it and restating the widened signature requires no new design intent or implementation evidence.

## Issue 2: The K ~ R exclusion on Emit_K is asserted but never enforced by any contract clause
Reason: Internal. The design decision (wrapper-only retraction, with sterilization-containment rationale) is already committed in S3; the fix is mechanical enforcement of it — adding a `K ≁ R` precondition using machinery the note already owns (CoverageEqualityDecidable against the shipped representative, the established rejection semantics) and re-anchoring two citations. Neither channel can inform how to enforce a policy the note itself originated.

## Issue 3: I0's inseparability rationale is false as stated
Reason: Internal. The review itself notes the conclusion is adequately grounded by the assertion-as-subtree argument and the Gregory/Nelson evidence already present in I0; the fix is scoping or deleting one overreaching supporting sentence, using counterexamples drawn entirely from the note's own surfaces (DR's single-tuple scope, Observe results, the enumeration predicates).

## Issue 4: Meta-prose and cross-section duplication (anti-bloat)
Reason: Internal. Pure prose trimming of enumerated instances; no claim content changes, so neither design intent nor implementation evidence bears on it. (Per the anti-bloat caution: none of the listed cuts carries a primary-source attribution, so no Nelson/Gregory citation is at risk.)
