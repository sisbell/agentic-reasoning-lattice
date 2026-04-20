# Revision Categorization — ASN-0029 review-1

**Date:** 2026-03-11 08:54

## Issue 1: D17 type error in FINDDOCSCONTAINING
Category: INTERNAL
Reason: The fix is a notational correction — expanding span membership into an address-range test. All definitions needed (spans, I-addresses, tumbler ordering) are already present in the ASN and ASN-0001.

## Issue 2: Σ.pub has no specified initial value, no frame conditions, and no transition operation
Category: INTERNAL
Reason: The ASN's prose already establishes that new documents are private, and D10/D11 describe publication semantics completely. The missing pieces are mechanical: specifying initial values, adding frame conditions, and wrapping the already-described semantics into a PUBLISH operation with pre/post/frame.

## Issue 3: D10 "standard operations" is undefined
Category: NELSON
Reason: The qualifier "standard operations" reflects a design choice about whether publication permanence is absolute or admits exceptions. Nelson's intent regarding withdrawal conditions determines whether D10 should be unconditional or scoped.
Nelson question: Is the permanence of publication absolute — once published, always published with no mechanism for reversal — or did you intend withdrawal to be possible under specific conditions, and if so, what distinguishes a withdrawal from a standard operation?

## Issue 4: D5(a), D5a, and D15 state the same property at three inconsistent strengths
Category: INTERNAL
Reason: The ASN already contains the resolution — Nelson's quote about the cooperative model and Gregory's observation that the backend unconditionally accepts any account. The fix is choosing D5a (the conditional formulation) as the honest one and eliminating the redundant D15, all derivable from existing content.

## Issue 5: D13 uses `session` in a formal property after declaring sessions to be implementation
Category: INTERNAL
Reason: The fix is a reformulation: parameterize CREATENEWVERSION by the requester's account address instead of referencing `session`. The abstract concepts needed (account addresses, document ownership) are already defined in the ASN.

## Issue 6: D14 claims ≺ forms a forest, but ≺ as defined is the ancestor relation
Category: INTERNAL
Reason: This is a mathematical error in the definition — ≺ as stated is a transitive ancestor relation, not the covering relation. The fix (redefine as immediate parent or state the claim about the Hasse diagram) is derivable from the tumbler hierarchy already defined in ASN-0001.

## Issue 7: D12 missing explicit precondition
Category: INTERNAL
Reason: The required precondition `d_s ∈ Σ.D` follows directly from the postconditions referencing `Σ.V(d_s)`, which is only defined for existing documents. Purely mechanical.

## Issue 8: No concrete example verifying postconditions
Category: GREGORY
Reason: Constructing a worked example for D12/D13 requires confidence in how version addresses are actually allocated — particularly whether the sub-document tumbler field increments by 1 and what the concrete address looks like when versioning across accounts. Gregory's implementation knowledge anchors the example in real allocation behavior.
Gregory question: When CREATENEWVERSION is called on an own-account document (e.g., `1.0.1.0.3`), what concrete tumbler address does the version receive — is it `1.0.1.0.3.1` for the first version, `1.0.1.0.3.2` for the second, and does the sub-document field always start at 1?
