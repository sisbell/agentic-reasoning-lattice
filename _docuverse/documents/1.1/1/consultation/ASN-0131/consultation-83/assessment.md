# Channel Assignment — ASN-0131 review-83

**Date:** 2026-06-14 15:21

## Issue 1: RE-UDIST's decisive bearing on Open Question 1 is proved-but-underived
Reason: Neither channel is needed — the fix is a purely algebraic observation fully derivable from claims already present (`clip_W`, `touch_W`, image union-distributivity), and the review itself supplies the witnessing counterexample from RE-UDIST-∩. The fix surfaces that RE-UDIST is reading-dependent; it does not resolve OQ1's faithfulness question, so no design-intent input is required.

## Issue 2: RE-NCD introduction enumerates its downstream consumers
Reason: Purely editorial — delete the consumer-inventory/placement sentence and state the lemma directly. No design intent or implementation evidence bears on a prose deletion.

## Issue 3: prefix-antichain re-derived inline, then equated to a foundation lemma, behind scaffolding prose
Reason: Compression of scaffolding and citation cleanup; the substantive antichain content rests on already-cited sibling-ASN foundation lemmas (ASN-0093 sub-allocator discipline, ASN-0086 R0a), and judging their scope is a matter of reading those spec documents, not consulting the implementation or design intent.
