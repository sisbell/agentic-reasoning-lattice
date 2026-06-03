# Channel Assignment — ASN-0071 review-19

**Date:** 2026-06-02 23:41

## Issue 1: PrefixConfinement (C0a) invoked outside its stated preconditions
Reason: The fix is internal — replace the C0a citation with a direct induction generalizing the position-1 TumblerAdd prefix-copy + T1 trichotomy argument already present in the Resolution section. No design intent (Nelson) or implementation behavior (Gregory) is at stake; the required lemma is purely a consequence of the ASN's own machinery (TumblerAdd, T1, the `actionPoint(ℓ) = #u` precondition).
