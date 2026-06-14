# Channel Assignment — ASN-0134 review-45

**Date:** 2026-06-14 14:29

## Issue 1: The "clause 7 is the one non-per-home operation-level clause" classification is restated at four sites
Reason: Pure editorial deduplication. The classification of clause 7 (non-per-home, per-coverage-class, operation-level, role-distinct from 2/5/6) is already fully argued in the note's own content (clause 7 body, §4 instance (i), G2); collapsing the restatements in the post-MIC paragraph and the claims-table row is a structural edit requiring no design intent or implementation evidence.

## Issue 2: The shared-frontier / collision-free conditional is re-derived in full at five sites
Reason: The conditional and both its ground cases (ASN-0047's `A_doc` rule, Gregory's `max_child + 1`) are already derived and cited within §4 and H3, and the review affirms the conditional is correct — the fix only collapses redundant re-derivations into citations and trims MIC clause 2 / SAFE(c) to references. No new intent or evidence is needed; the combination is established by H3 (commutation) plus G1 (linearization) already present.

## Issue 3: A6's per-state package presents as exhaustive but isn't, and the enumeration does not carry the claim
Reason: The fix restates A6's claim via the reachability + transfer-lemma route A6 itself already names, cites a few representative members, and drops the exhaustive-list framing and the `P2`/`R2` parenthetical — all internal. The single factual input, that ASN-0086's `R0a` (FlatLinkDomain) is a single-state lemma of the same character, is dependency-ASN corpus content the reviewer already supplied; it is neither Nelson's design intent nor Gregory's implementation, so no channel applies.
