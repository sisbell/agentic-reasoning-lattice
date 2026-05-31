# Channel Assignment — ASN-0084 review-103

**Date:** 2026-05-30 20:50

## Issue 1: Defensive "derived vs assumed" justification lodged in the Properties table
Reason: Pure editorial fix — reducing the table row to clauses (i)–(iv) and dropping the parenthetical requires only the ASN's own content, since Width-positivity is already derived in the Consequences block. No design intent or implementation evidence needed.

## Issue 2: The "shift preserves subspace" fact is re-argued inline at four sites
Reason: Factoring the OrdShiftHom (a) instance into one named consequence and citing it is an internal restructuring; the fact and its four uses are already present and correctly cited in the ASN.

## Issue 3: EXT-VAC(a) is a consequence with no proof consumer
Reason: Deciding to demote EXT-VAC(a) into the boundary worked example (its only consumer) is derivable by inspecting the ASN's own proof-dependency structure; no external channel bears on this placement choice.
