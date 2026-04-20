# Revision Categorization — ASN-0002 review-4

**Date:** 2026-03-06 14:04

## Issue 1: AP5 is formally identical to AP
Category: INTERNAL
Reason: The fix is choosing between strengthening the formula or relabeling the property — both options are derivable from the ASN's own definitions of AP0, AP1, AP2, and AP.

## Issue 2: AP4 implies AP2 only with an unstated premise
Category: INTERNAL
Reason: Partition disjointness is already stated in the ASN's prose ("text addresses begin with subspace identifier 1, link addresses with identifier 2"). The fix is to formalize what is already present.

## Issue 3: Boundary cases absent from operation analysis
Category: INTERNAL
Reason: Zero-width behavior for each operation is determined by the existing formal definitions — AP2 is vacuously satisfied, V-space effects vanish, etc. For CREATELINK with empty endsets, the type structure (endset = set of spans, empty set is valid) already determines the answer.

## Issue 4: REARRANGE precondition proposed but not adopted
Category: INTERNAL
Reason: The ASN already contains both the analysis of the cross-subspace violation and the judgment that it is a missing guard. The fix is resolving the internal contradiction — either adopt the precondition or weaken the language.

## Issue 5: CREATENEWVERSION proof depends on an undefined Content type
Category: INTERNAL
Reason: The ASN already describes the content types (text content in text_subspace, link structures in link_subspace) and already states that POOM orgls are not content atoms. The fix is to formalize the sum type from information already present.

## Issue 6: AP10 missing postcondition for new version's link subspace
Category: INTERNAL
Reason: The ASN already states in prose that "the new version begins with text content only" and that the link subspace is not copied. The fix is adding the formal postcondition for what is already established.
