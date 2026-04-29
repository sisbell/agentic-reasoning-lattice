# Revision Categorization — ASN-0047 review-1

**Date:** 2026-03-17 02:03

## Issue 1: J0 claimed as derivation from S7a but is a new invariant
Category: INTERNAL
Reason: The fix is reclassifying J0's logical status from "derived from S7a" to "new axiom." The justification material — Nelson's description of content entering through documents — is already quoted in the ASN. No new evidence needed; the restructuring is purely about logical honesty.

## Issue 2: K.μ⁺ and K.μ⁻ do not state value preservation for unaffected mappings
Category: INTERNAL
Reason: The missing value-preservation constraints are implicit in the definitions of "extension" and "contraction" already in the ASN, and are required by the completeness argument (replacement = K.μ⁻ + K.μ⁺) that the ASN itself makes. Pure formalization gap.

## Issue 3: Entity set partition is not exhaustive without element-level exclusion
Category: INTERNAL
Reason: The ASN already places elements in dom(C) and defines E using three level predicates. The fix is stating the exclusion `¬IsElement(e)` for e ∈ E explicitly — a constraint that follows from the ASN's own definitions and the distinction between E and dom(C) already drawn in the state model section.

## Issue 4: P4 lacks base case and systematic verification
Category: INTERNAL
Reason: The base case (empty initial state) and per-transition case analysis are mechanical consequences of the elementary transition definitions and frame conditions already specified in the ASN. All needed properties (J1, monotonicity of K.μ⁻, ran-preservation of K.μ~, frame conditions) are already stated.

## Issue 5: Frame conditions and coupling constraints use incompatible scopes without clarification
Category: INTERNAL
Reason: The ASN uses reading (A) — frames describe individual transitions, coupling describes required composition — consistently throughout. The fix is adding an explicit statement of this compositional semantics and noting ordering constraints that follow from preconditions already specified (e.g., S3 requires K.α before K.μ⁺). No external evidence needed.
