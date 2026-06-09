# Channel Assignment — ASN-0120 review-11

**Date:** 2026-06-09 11:34

## Issue 1: Reachability precondition carries a use-site inventory
Reason: Pure editorial trim — drop the downstream-invariant enumeration and stop at the precondition. The citations already stand where used in the ASN's own text; no design intent or implementation evidence is involved.

## Issue 2: ML2 duplicates ML1's load-bearing equation
Reason: Reconciling two of the ASN's own claims — the set equation is identical, so the fix is to relocate ML2's only distinct content (cardinality non-observability) or restate it. Both claims and their supporting reasoning are already present in the ASN.

## Issue 3: Meta-prose on what is *not* observable, deferring to the implementation note
Reason: Prose reduction of a parenthetical paragraph to a clause, working entirely from the ASN's already-stated coverage guarantee and its own L5/LP21 citations. Internal.

## Issue 4: Open Question 4 is already answered by ML9 plus a foundation
Reason: The question's negation is ML9 and its resolution is ASN-0098 LP17/LP18, both already cited in this ASN; deciding to remove or reframe is derivable from the ASN's own content and a verified foundation. Internal.
