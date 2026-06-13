# Channel Assignment — ASN-0123 review-7

**Date:** 2026-06-13 00:13

## Issue 1: Node-tier cross-owner fork — V9(b) ownership is asserted, not established
Reason: The fix is a choice among purely formal options — restrict the cross-owner precondition to account-tier forkers (`zeros(pfx(π)) = 1`) or restate V9(b) as "the unique maximal-length coverer" — and the note's own single-mint guarantee (G1) plus the cited ASN-0042 axioms (O1a, O2, O5, O15) already force exclusion of the node-tier path. The node-tier/account-tier distinction is an artifact of the prefix model Nelson never reasoned in, and deviation 4 shows the implementation leaves cross-owner placement uncoverned anyway, so neither channel can adjudicate the choice.

## Issue 2: V9w's first conjunct cites a composite-boundary property at an unconstrained start state
Reason: Purely a foundation-citation correctness fix — replace the composite-boundary P4★ citation with the persistence argument (J1★ at the recording boundary + P2), exactly the salvage route the review item itself spells out, using only foundations already cited in the note. Neither design intent nor implementation behavior bears on which invariant justifies `(a, d_src) ∈ R`.
