# Revision Categorization — ASN-0079 review-1

**Date:** 2026-03-23 01:00

## Issue 1: SearchConstraint terminology is misleading for type queries
Category: INTERNAL
Reason: The formal definition is already correct ("non-empty finite set P ⊂ T"). The fix is dropping or qualifying the informal gloss "of I-addresses," using L9/L10 references already cited in the ASN.

## Issue 2: F6 pagination is undefined at the boundary
Category: INTERNAL
Reason: This is a missing base case in a mathematical definition. The fix — adding page(Q, c, N) = ⟨⟩ when the index set is empty — is a standard totality repair requiring no external evidence.

## Issue 3: No concrete example
Category: INTERNAL
Reason: The review provides a sufficient scenario sketch, and all definitions needed to instantiate it (satisfaction predicate, projection, transclusion transparency) are already formalized in the ASN. Constructing the example is mechanical application of existing definitions.
