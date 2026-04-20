# Revision Categorization — ASN-0047 review-13

**Date:** 2026-03-17 08:04

## Issue 1: Contains(Σ) used before definition in the valid composite definition
Category: INTERNAL
Reason: This is a presentation ordering issue entirely within the ASN. The definition of Contains(Σ) already exists in the document; it just needs to be moved earlier. No external evidence required.

## Issue 2: K.μ~ decomposition fails on empty arrangements
Category: INTERNAL
Reason: The boundary case and its resolution are derivable from the ASN's own definitions of K.μ⁻, K.μ⁺, and K.μ~. The fix is a qualification of an existing claim using already-stated preconditions.

## Issue 3: J1 and J1' quantifier domain unbound
Category: INTERNAL
Reason: The prose already states the correct domain ("quantify over E'_doc, not E_doc") and J0 demonstrates the correct pattern. The fix is transferring an existing prose restriction into the formal notation.
