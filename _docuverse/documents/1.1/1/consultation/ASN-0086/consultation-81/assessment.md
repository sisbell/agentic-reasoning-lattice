# Channel Assignment — ASN-0086 review-81

**Date:** 2026-05-31 14:31

## Issue 1: R0 re-verifies the entire L/S/M/C catalog that K.λ already guarantees by construction
Reason: Internal. The fix is an editorial reduction — cite K.λ's by-construction preservation guarantee (already asserted in the ASN from ASN-0093) once and verify only the arity-3/`e₃=K` specialization. No design intent or implementation evidence is needed to delete a redundant per-invariant walk.

## Issue 2: R7a's "Per-step substrate-invariant discharge" block duplicates Issue 1 across two step types
Reason: Internal. Collapsing the per-step catalog enumeration into "each replay step is a primitive K-op preserving the full catalog by its ASN-0093 contract" is structural condensation derivable from the ASN's own statement of the K-op contracts.

## Issue 3: The L14/L14a SC-NEQ argument is written out verbatim three times
Reason: Internal. Factoring the identical SC-NEQ/L14/L14a discharge into one named sub-lemma (or citing SD, ASN-0093) is a refactor of content already present; no channel needed.

## Issue 4: R0a-Cor1's "Substantive postconditions" enumerate downstream consumers
Reason: Internal. Dropping the "consumed downstream by..." use-site inventory while retaining the two postconditions is pure editing of existing material.

## Issue 5: R6b's Justification elaborates an alternative definition the ASN explicitly does not adopt
Reason: Internal. The adopted reading (single-pass existential over `L_R^Σ`) is in the ASN; deleting the counterfactual parity/fixpoint essay requires nothing external.

## Issue 6: Design Note: NonTupleRetractionViaClassifierTuples is a "why the restriction exists" essay and a deferral target
Reason: Internal. The operative facts (`nullified(Σ) ⊆ A_rel^Σ`, classifier-tuple recovery) are substrate-level and already stated; the fix is to fold them into the Definition and delete the surrounding essay — a condensation, not a re-verification of design intent.

## Issue 7: Multiple sections defer to the same downstream location (WP Case 2)
Reason: Internal. Consolidating three forward-references to a single definitional home is a structural cleanup using only the ASN's existing cross-references.

## Issue 8: R0's verification redundantly recites the L-permissions as "not requiring preservation" — repeated in R5-Cor and R7a
Reason: Internal. Removing the thrice-repeated permission recital (or reducing to one global sentence near the substrate-conforming-layer Definition) is editorial; permissions impose no obligation by definition already stated.
