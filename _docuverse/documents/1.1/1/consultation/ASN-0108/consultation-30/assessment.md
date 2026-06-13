# Channel Assignment — ASN-0108 review-30

**Date:** 2026-06-13 03:00

## Issue 1: The "content-position key" the hazard walks use is not the key the implementation evidence describes — one is permanent, the other mutable
Reason: The disambiguation turns on what the udanax-green insertion-sort actually keys on — a permanent I-address boundary (which makes W5/W8/W9c vacuous, option b) or a mutable V-position (which makes the walks valid under a corrected definition, option a). Choosing between the reviewer's two required options requires evidence from the implementation, so Gregory is needed; Nelson's intended key (the address key) is already settled in the note.
Gregory question: When the link-search builds its result list by insertion-sort during the index traversal, does the sort key it compares on resolve to the matched content's permanent I-address (immutable, surviving rearrangement and orphaning) or to that content's current V-position within the consulted document (which moves under K.μ~ and disappears under K.μ⁻)?

## Issue 2: The W9 "global guarantee" is mis-stated and contains a self-contradiction
Reason: This is a logic/precision fix derivable from the note's own claims — the local fact already establishes `After(next-cursor) = ∅` (making the quantifier vacuous), and the W5 cut-point walk already shows the skipped `L_2` sits behind the final cursor, so the restatement to a whole-pass completeness property and the corrected explanatory sentence follow from material already present.

## Issue 3: Duplicated argument across sections, and summary-table rows that restate full claims
Reason: Purely editorial deduplication and table compression — consolidating the orthogonality-of-allocation point into W5 with a reference from W8, and shortening the W5/W9b table rows to one-line hooks, all derivable from the existing text with no design-intent or implementation question at stake.
