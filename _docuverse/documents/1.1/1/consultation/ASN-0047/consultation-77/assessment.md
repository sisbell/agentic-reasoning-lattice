# Channel Assignment — ASN-0047 review-77

**Date:** 2026-05-17 11:48

## Issue 1: J1★ formulation has incorrect operand in negated existential
Reason: Pure logical fix derivable from the ASN's own content — J1'★ already uses the correct form `M(d)(v) = a` in the analogous slot, and the explanatory prose confirms the intent.

## Issue 2: Defensive axiom commentary dwarfs axiom content
Reason: Editorial trimming of meta-commentary around axioms whose statements remain unchanged; no new design or implementation input needed.

## Issue 3: Document-ordering justification at D-SEQ★
Reason: Pure document reorganization — move D-SEQ★ ahead of its first consumer and remove the staging-justification prose. Internal.

## Issue 4: K.δ table followed by prose restating identical content
Reason: Editorial choice between two equivalent presentations of the same content; the spec itself acknowledges the duplication. Internal.

## Issue 5: Consultation evidence in spec body
Reason: Editorial relocation of evidence prose to a Design provenance section or reasoning doc; the question is where evidence lives, not what it says. Internal.

## Issue 6: Worked example "Rejection model" paragraph
Reason: Remove meta-paragraph from a worked example slot; convention can be stated once at the *Elementary transitions* heading if needed. Internal.

## Issue 7: K.μ⁻ "Worked sub-case" inside precondition
Reason: The case analysis already proves (B)'s necessity; the worked sub-case is illustrative duplication and can be removed without losing content. Internal.

## Issue 8: Repeated S8 discharge across K.μ⁺/K.μ⁻/K.μ~ cases
Reason: Editorial refactoring — factor the identical S8 discharge into a single named lemma cited from each transition case. Internal.

## Issue 9: K.μ~ corollary placement justifications
Reason: Reorder the K.μ~ section so dependencies are linear and remove the placement-commentary prose. Internal.

## Issue 10: Properties Introduced table commentary
Reason: Remove meta-commentary about table partitioning; the structure is self-evident from headings. Internal.
