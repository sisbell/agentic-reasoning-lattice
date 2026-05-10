# Revision Categorization — ASN-0042 review-8

**Date:** 2026-03-15 22:32

## Issue 1: O6 proof — biconditional asserted without showing the reverse direction
Category: INTERNAL
Reason: The missing reverse direction (pfx(π) ≼ acct(a) ⟹ pfx(π) ≼ a) follows from prefix transitivity through acct(a) ≼ a, which is derivable from the acct definition already present in the ASN. No external evidence needed.

## Issue 2: O2 well-definedness — existence of maximum in covering set
Category: INTERNAL
Reason: The finiteness argument uses only definitions already in the ASN: prefixes of a are determined by their length (at most #a values), and O1b gives at most one principal per prefix. Pure reasoning gap, no external evidence needed.

## Issue 3: O10 — property statement makes unformalizable claim
Category: INTERNAL
Reason: The ASN itself identifies the issue — "a relationship that belongs to the content model, not the ownership model" — and the fix is editorial: align the property statement text with the formal conditions (a)-(c) already present. No design-intent or implementation question arises.
