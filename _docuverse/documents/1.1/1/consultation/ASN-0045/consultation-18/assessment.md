# Channel Assignment — ASN-0045 review-18

**Date:** 2026-05-28 20:06

## Issue 1: at-least-one enumeration silently uses trichotomy (NAT-order) without citing it
Reason: The fix is internal — it requires adding citations to NAT-order and NAT-addcompat (both ASN-0034 foundation axioms already referenced by the ASN) and spelling out the case-split chain. No design intent or implementation evidence is needed; the required axioms and the logical structure are already within the ASN's foundation.

## Issue 2: Account lists T4c as a base-biconditional dependency, contradicting the treatment given to the other three predicates
Reason: The fix is internal — it is a pure consistency edit applying the same T4c caveat already stated for Node/Document/Element to Account's base biconditional and scoping T4c/T4b/T3 to the rename-equivalence postcondition. The ASN's own reasoning already establishes T4c does no work in the base biconditional.
