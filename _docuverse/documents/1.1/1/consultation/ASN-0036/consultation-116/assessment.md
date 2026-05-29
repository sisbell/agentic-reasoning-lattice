# Channel Assignment — ASN-0036 review-116

**Date:** 2026-05-28 20:46

## Issue 1: S5 states both constructions twice
Reason: Pure deduplication of two identical construction passages within the same property; no design intent or implementation evidence is at stake. Internal to the ASN.

## Issue 2: S7 well-definedness paragraph justifies its dependency list instead of arguing
Reason: Collapsing defensive dependency-bookkeeping prose into one sentence requires only the ASN's own S7b/T10a.4 citations. Internal to the ASN.

## Issue 3: `subspace_I` and `subspace` introductions narrate document structure
Reason: Replacing placement narration with the direct definition and precondition uses only content already present in the ASN. Internal.

## Issue 4: Hypothetical future-subspace justification before D-CTG
Reason: Deleting the parametric-extension speculation and retaining the `S = 1` binding is a pure excision; nothing about design intent or implementation is needed. Internal.

## Issue 5: ValidInsertionPosition split-rationale is design commentary
Reason: Removing the authoring-decision justification leaves the two self-evident Formal Contracts; derivable from the ASN alone. Internal.

## Issue 6: S8a invokes T4 on a bare element field that is not a T4 address
Reason: The fix—dropping T4 from the positivity derivation in favor of the element-field commitment plus T0/NAT-discrete—is settled by the ASN's own proof and ASN-0034's T4c semantics already cited. Internal.

## Issue 7: S9 restates S0 with no formal content
Reason: Choosing between adding a family-quantified statement (the arrangements quantification is already implicit in the ASN) or demoting to a corollary is an internal structuring decision derivable from S0 and the existing arrangement model. Internal.
