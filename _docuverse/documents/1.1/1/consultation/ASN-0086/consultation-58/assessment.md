# Channel Assignment — ASN-0086 review-58

**Date:** 2026-05-19 09:06

## Issue 1: R0a's non-disciplined counterexample is computationally inconsistent
Reason: Pure computational/proof error. The fix is mechanical — replace the bogus witness `a₁.0.1.1` (which violates L1's `zeros = 3`) with `a₁.1` or `a₁.2`, both derivable from L1 and the substrate emission primitive already in the ASN. R0a's structural argument is unchanged.

## Issue 2: R7a's substrate-wide extension of L12/L12a is asserted without justification
Reason: The reviewer offers two equally internal fixes — either add a conformance precondition to R7a's quantifier, or supply the short "any layer publishing over substrate state must preserve substrate invariants" argument. Both routes are structural choices about how to frame the categorical claim and require no external evidence; the layering model is already articulated in the ASN.

## Issue 3: "Substrate guarantee" framing for Nullify's single-tuple scope is misleading
Reason: Pure terminology/framing fix. The ASN already distinguishes substrate primitive from sibling-frontier discipline (Implementation Notes); rewording "substrate guarantee" to "guarantee under the sibling-frontier discipline" aligns Nullify's language with the layering the rest of the note maintains.

## Issue 4: WP Case 2 omits the regime-distinction's appearance in R6c Consequence (d)
Reason: The unit-depth retraction discipline is already declared in the Implementation Notes and the relational layer's commitment already pins Emit_R to Nullify. Stating explicitly that regime (ii) is structurally impossible under the layer's operations and simplifying the wp formula accordingly is an internal consolidation of pieces already present in the ASN.
