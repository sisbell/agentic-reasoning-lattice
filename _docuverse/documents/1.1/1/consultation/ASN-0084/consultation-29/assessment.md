# Channel Assignment — ASN-0084 review-29

**Date:** 2026-05-15 12:33

## Issue 1: m_1 = 2 attributed to ASN-0036 but not established there
Reason: The fix can be stated as an explicit assumption (internal), but grounding the assumption is stronger if we know what Nelson intended for the text subspace depth and/or what udanax-green actually fixes. Both channels inform whether to ground or merely stipulate.
Nelson question: Did Nelson's design fix the text subspace at depth 2, or leave the depth operator-chosen subject only to m ≥ 2?
Gregory question: Does the udanax-green implementation fix the text subspace at depth 2, or does it permit (or instantiate) text subspaces with m_1 > 2?

## Issue 2: R-WP postcondition is trivially true
Reason: The fix is internal — selecting a non-trivial postcondition from material already in the ASN (R-BLK construction, invariant-preservation paragraph, canonical-partition bounds) or relabelling R-WP as a corollary. The reviewer's three candidates are all derivable from existing ASN content.
