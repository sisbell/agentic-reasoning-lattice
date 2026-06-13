# Channel Assignment — ASN-0108 review-51

**Date:** 2026-06-13 10:56

## Issue 1: W0 requires κ injective but not *total*; the least-covered-I-address key is partial on Match
Reason: Stating totality as a W0 premise is internal (a logical fact about total orders), but the substantive part — resolving the contradiction for the least-covered-I-address key without the forbidden matched-slot fix — turns on whether a fixed designated slice can be faithfully total, which depends on how the udanax-green link index orders a link that reaches the result set only through its type endset. That is implementation evidence, and the key is explicitly Gregory's reading of the implementation.
Gregory question: Can udanax-green create a link with empty from and to endsets that still appears in link-search results (matching via its type endset), and if so, what I-address positions such a link in the spanfilade/`onlinklist` result order — i.e., is every returned link guaranteed a non-empty covered I-address on the slot that drives ordering?

## Issue 2: Trailing-gloss restatement (anti-bloat)
Reason: The fix is fully specified by the review — keep the Nelson-analogy sentence, delete the named restating clause — and is a pure prose edit derivable from the ASN's own text; no design intent or implementation evidence bears on it.
