# Channel Assignment — ASN-0042 review-122

**Date:** 2026-05-30 05:24

## Issue 1: O7(c) postcondition overstates the recursion as identical constraints
Reason: The proof body already establishes the correct claim (same five-condition gate, but (ii)/(iv)/(v) re-evaluated against the delegation state). The fix only requires aligning the summary sentence with the ASN's own proof — no design intent or implementation evidence needed.

## Issue 2: O7(c) proof carries multi-paragraph meta-prose classifying when conditions bind
Reason: Pure editorial deduplication — collapsing three restatements of the same auto-discharge/rebind fact into one. The load-bearing claim is already present in the ASN.

## Issue 3: O17b definition slot enumerates downstream consumers
Reason: Removing the parenthetical consumer-enumeration is internal; the dependency direction is already recorded in the O18 and Freshness-(v) derivation citations within the same ASN.

## Issue 4: "Unilateral O10★" restates the existing postcondition
Reason: The duplicate existence claim and its witness are both already in the ASN; the "performed by π alone" delta is established by the proof's Per-baptism authorization paragraph. Folding/removing is a self-contained editorial merge.

## Issue 5: NamespacePrincipalExclusivity adds no claim beyond O18 + Freshness-(v) + B0
Reason: The corollary is the contrapositive of Freshness-(v)'s freshness conjunct under B0 monotonicity — all three inputs are already in the ASN, so removing or shortening it is derivable internally without external consultation.
