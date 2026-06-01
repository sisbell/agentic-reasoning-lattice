# Channel Assignment — ASN-0047 review-251

**Date:** 2026-06-01 13:55

## Issue 1: Non-lineage of distinct nodes' account sub-allocators is asserted, not derived
Reason: The preferred fix is a tumbler-algebra derivation showing distinct node tumblers yield prefix-incomparable `inc(N,2)` bases (the zero separator at position `#N₁+1` in `[N₁.0.1]` diverges from `N₂`'s nonzero continuation, even when `N₁ ≼ N₂`), discharging T10a.5's precondition. This follows entirely from T4b/TA5 and the `zeros=0` node form already cited in the ASN — derivable internally.

## Issue 2: Per-state vs. composite-boundary distinction restated three times
Reason: Pure anti-bloat editorial consolidation — state the distinction once in the section preamble and cite it; no design intent or implementation evidence is involved.

## Issue 3: P4a discharge mechanism deferred to the same location from three sites
Reason: Pure anti-bloat editorial fix — discharge P4a once in its definition box and have Class (b) and the matrix cite by name; entirely internal to the ASN's own organization.

## Issue 4: TS-family citation in K.μ⁺_L is imprecise
Reason: The reviewer already identifies the single load-bearing lemma (shift length-preservation, `#shift(v,n) = #v`); replacing the TS1–TS5 inventory with the precise citation is derivable from ASN-0034's already-referenced lemma set, requiring no external channel.
