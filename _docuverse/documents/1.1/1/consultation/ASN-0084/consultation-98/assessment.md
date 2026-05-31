# Channel Assignment — ASN-0084 review-98

**Date:** 2026-05-30 19:53

## Issue 1: The "B′ is not maximal" caveat is restated five times
Reason: Purely editorial deduplication — collapse five restatements of an internal scoping caveat into one at the R-BLK statement. No design intent or implementation evidence is involved; the distinction is already fully established within the ASN.

## Issue 2: Use-site framing and forward-defense in place of plain statements
Reason: A prose-rephrasing fix — assert the EXT-VAC right-exterior implication directly and strip use-site narration from the S8-cons/run-partition labels. The underlying facts already hold in the ASN; only the framing changes.

## Issue 3: EXT-VAC right-exterior cites the wrong premise
Reason: A self-contained citation correction — the conclusion follows from D-SEQ (V_S(d) = {[S,1],...,[S,N]}), already stated in the ASN, rather than R-PRE(iv). Swapping the cited premise needs no external input.
