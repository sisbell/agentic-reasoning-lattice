# Channel Assignment — ASN-0120 review-21

**Date:** 2026-06-11 05:04

## Issue 1: ML9's future-state consequence cites only half its premises
Reason: The review itself notes every premise for the lift is already in the ASN — the subspace exclusion (LP-Fin Corollary, LP-Sub, L0) and the freshness exclusion (LP19a) are all cited in Fact (a) and the stability sentence; the fix is just assembling the existing chain at all later states. No design intent or implementation evidence is needed.

## Issue 2: the empty from/to-resolution boundary is determined by the contract but never stated, and the body is in tension with itself about it
Reason: The formal consequences (recovery equation forcing `e_j = ∅`, L3 satisfaction, inertness in ML9's wp) are derivable internally, but the "pick one" decision — admit empty from/to resolution or strengthen `enabled` to reject it — turns on whether the design sanctions one-sided/degenerate links, and the implementation note covers only the empty *type* path, not empty from/to.
Nelson question: Does the design intend a link whose from or to endset names no content to be a legitimate (degenerate, one-sided) link, or must both non-type endsets always attach to at least some content?
Gregory question: When a from or to V-span set passed to CREATELINK resolves to an empty sporgl set (all named positions deleted), does the implementation reject the call or store the link with an empty endset, as the implementation note records for the type slot?
