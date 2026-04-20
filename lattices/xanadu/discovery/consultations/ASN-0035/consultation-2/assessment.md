# Revision Categorization — ASN-0035 review-2

**Date:** 2026-03-14 15:40



## Issue 1: N5 formal statement is weaker than the intended property
Category: INTERNAL
Reason: The fix is fully derivable from the ASN's own content — BAPTIZE's postcondition already specifies that the first child has last component 1, and the prose explicitly states the initial-segment property. This is a matter of aligning the formal quantifier with the already-present definitions.

## Issue 2: N8 verification omits N2 from the state-dependent invariant enumeration
Category: INTERNAL
Reason: The preservation argument for N2 already exists in the ASN (the inductive derivation in N2's own section). The fix is adding a back-reference to that existing proof in N8's enumeration — no external evidence needed.

## Issue 3: N15 introduces authorization concepts with no formal integration
Category: NELSON
Reason: The core question is whether allocation authority should be formalized as a precondition on BAPTIZE at this layer or deferred to the account ontology. This is a design-intent question about where authorization enters the specification — Nelson's architectural decision, not an implementation question.
Nelson question: Should the node ontology formally constrain who may baptize children under a node (via an abstract authorization predicate on BAPTIZE), or is allocation authority purely an account-level concern that belongs in a downstream ASN?
