# Channel Assignment — ASN-0075 review-74

**Date:** 2026-06-03 11:43

## Issue 1: The wp section restates "boundary conjunct is not part of the weakest precondition" four times
Reason: Pure editorial deduplication — collapsing four restatements of a fact already proven within the ASN (D-WIT/D-EXH hold only at composite boundaries) into one statement. No design intent or implementation evidence bears on the prose structure.

## Issue 2: Output-half finiteness derived in two places
Reason: The finiteness fact rests entirely on C-fin (ASN-0047) and S8-fin (ASN-0036), both already cited in the ASN; consolidating the two derivations is a self-contained editorial fix requiring no external channel.
