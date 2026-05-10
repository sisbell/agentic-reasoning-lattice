# Revision Categorization — ASN-0006 review-2

**Date:** 2026-03-06 22:00

## Issue 1: Position space undefined; TC7 and TC8 consistency depends on unstated assumption
Category: INTERNAL
Reason: The ASN already contains the subspace ordering information (V < 1.0 for links, V ≥ 1.0 for text) and tumbler structure needed to define `Pos`, `⊕`, `link_subspace`, and `size`, and to derive TC8 from TC7. The fix is formalizing what is already stated informally.

## Issue 2: Precondition — source V-span coverage ambiguous
Category: INTERNAL
Reason: This is an internal consistency gap between the prose ("must resolve") and the formal predicate (`≠ ∅`). The downstream properties (TC9, TC7's width `w`, TC10) are all stated within the ASN, so the author can choose full or partial coverage and align everything without external evidence.

## Issue 3: TC2 uses undefined predicate "p is new"
Category: INTERNAL
Reason: Pure notational fix. The review provides the replacement (`p ∈ [p₀, p₀ + w)`) which is derivable from the ASN's own definitions of insertion point and copied width.

## Issue 4: Concrete trace addresses do not match the declared address format
Category: INTERNAL
Reason: The ASN declares the format `Node.0.User.0.Document.0.Element` and the concrete trace uses incompatible 6-component addresses. The fix is aligning the trace with the declaration (or vice versa) and clarifying whether `fields(a).document` extracts a single component or a composite prefix — all information needed is already in the ASN.
