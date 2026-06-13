# Channel Assignment — ASN-0132 review-20

**Date:** 2026-06-13 11:56

## Issue 1: CN-ORPHAN states "the gap is exactly the orphans" against the wrong baseline
Reason: The fix is a set-algebra correction internal to the ASN: the union baseline (FL-REACH, already cited from ASN-0121) and the single-document baseline are both already named in the text, and the reviewer supplies the corrected relationship. Distinguishing the two gaps requires only the definitions of `discoverable_from`, orphans, and the FL-REACH union bound already present — no design intent or implementation evidence.

## Issue 2: CN-RETRACT restates the view/store distinction past the point it has been made
Reason: Pure anti-bloat prose trimming — cut the thematic restatement and closing flourish, keep the active-view/store sentence and the prior-view contrast. The substantive content and the CN-ENUM lean-point are entirely internal to the ASN; no channel needed.
