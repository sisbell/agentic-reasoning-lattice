# Revision Categorization — ASN-0026 review-1

**Date:** 2026-03-08 00:06

## Issue 1: P6 is formally identical to P0; P8 is formally identical to P1
Category: INTERNAL
Reason: The logical relationship between axioms and corollaries is derivable from the formal statements already present in the ASN. Reorganizing P6 as a derived classification and P8 as a corollary requires only the definitions in this document.

## Issue 2: P3 introduces an undefined term
Category: INTERNAL
Reason: The ASN's own explanatory text makes clear that P3 rules out transformed views. The fix — defining a retrieval function or restating as a constraint on operations — is derivable from the state model and operation set already defined.

## Issue 3: P4 is not a well-formed state invariant
Category: INTERNAL
Reason: The ASN's own prose already describes the intended property: independent INSERT operations never produce the same I-address regardless of content equality. The reformulation from vague "distinct identities" to an allocator constraint restates what the text already explains.

## Issue 4: P9 and P10 describe implementation representation, not abstract state
Category: INTERNAL
Reason: The review identifies the abstract content underlying P9 (INSERT preserves I-mapping at surviving positions) and the purely representational nature of P10 (coalescing is invisible at the abstract level). Both reformulations are derivable from the existing state model definitions.

## Issue 5: Mutable vs. immutable document-version ambiguity
Category: NELSON
Reason: The ASN uses "version" (implying immutability) but describes operations as mutations. Nelson's design intent determines whether operations mutate a document's working state (with versions as explicit snapshots via CREATENEWVERSION) or whether every operation produces a new immutable version identifier.
Nelson question: In the Xanadu design, does a document have a mutable working state that operations modify in place — with CREATENEWVERSION as the explicit act that creates a distinct immutable snapshot — or does every editing operation (INSERT, DELETE, REARRANGE) itself produce a new version?

## Issue 6: No base case for the invariant framework
Category: INTERNAL
Reason: The initial state (empty I-space, no documents) is straightforward from the definitions, and all properties hold vacuously. No external evidence needed.

## Issue 7: No concrete example
Category: INTERNAL
Reason: The ASN's own definitions of Sigma.I, Sigma.V, and the operations table provide everything needed to construct a worked example and verify properties against it.

## Issue 8: Cross-ASN forward references
Category: INTERNAL
Reason: Purely editorial — replacing ASN numbers with descriptive phrases requires only the operation names already listed in the ASN.

## Issue 9: Preservation obligation is over-broad
Category: INTERNAL
Reason: The classification of which properties are operation-relevant invariants vs. architectural constraints is derivable from the property definitions themselves. The review already identifies the partition; the ASN contains the reasoning.
