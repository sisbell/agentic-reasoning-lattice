# Channel Assignment — ASN-0094 review-27

**Date:** 2026-05-20 05:47

## Issue 1: R6 cited as a single property
Reason: Citation precision against ASN-0086's existing structure. The R6a/R6b/R6c/R6c-Corollary split is documented in ASN-0086; the reviser substitutes the specific sub-claim at each site. Internal.

## Issue 2: Direct ASN-0093 citation in `→` definition
Reason: Routing discipline through the substrate-conforming-layer scaffolding is already established by the ASN; this site just needs to follow the existing pattern (either via a named scaffolding clause or via ASN-0086's SubstrateConformingLayer Definition). Internal.

## Issue 3: Missing Classifier walkthrough
Reason: Mechanical exercise of the framework's existing definitions (Sh-conf, template body, rejection at clause (d)) at the simplest shape. The structure mirrors the existing Tuple-Classifier and Provenance walkthroughs with a single-letter substitution and the partition-vs-allocation rejection split. Internal.

## Issue 4: Resolution standalone walkthrough deferred
Reason: A choice between adding a hypothetical standalone example or hardening the prose disclaimer — both options are internal authoring decisions within Sh5(b)'s mechanical-derivation rule already in scope. Internal.

## Issue 5: Notational conflation in EffectiveWpSimplification walkthrough
Reason: Pure notation fix — ASN-0086's `L_R^Σ` tuple structure dictates that the first component is the tuple-address `b_1`, not the tuple `ρ_1`. Internal.

## Issue 6: EffectiveWpSimplification statement under-qualified
Reason: Statement-precision fix on the framework's own corollary, qualifying under the *Emit_K routing commitment*. The proof body already enforces the conditional; only the statement needs to be tightened. Internal.

## Issue 7: Duplicate-Nullify compatibility argument is prose, not theorem
Reason: Promoting existing prose to a labeled corollary, citing R6a and the audit-vs-active distinction already established in the ASN and inherited from ASN-0086. Internal reorganization.

## Issue 8: Sh4 Case B "no concurrent nullification" qualifier inherits depth gap
Reason: Clarifying the case decomposition's exhaustiveness against the existing K ≁ R vs K ~ R split (Case D absorbs the latter). One-sentence note from the existing proof structure. Internal.
