# Channel Assignment — ASN-0112 review-54

**Date:** 2026-06-10 22:35

## Issue 1: V9's converse direction is false — composition changes need not move the extent
Reason: The counterexample is built entirely from the ASN's own worked example and the definitions of `origin_d`/`reach_d`; the corrected statement (span is a function of the extremes of `O(d)`) follows from V1–V3 as already proven. No design-intent or implementation question remains open — the fix is a restatement to match what the ASN itself establishes.

## Issue 2: The V5/V6-dichotomy defense is stated three times
Reason: This is a structural deduplication — consolidating an argument already present in the V6 paragraph and deleting its repetitions. Purely editorial; no external input bears on it.

## Issue 3: V2 case 2 attributes a TumblerSub + TumblerAdd composite to TumblerAdd alone
Reason: The fix is a proof expansion using TumblerSub, TumblerAdd, and TA2 from ASN-0034, all already cited foundation material; the componentwise derivation is mechanical from those definitions. Neither design intent nor implementation evidence is at issue.

## Issue 4: V12's count-recovery chain stops one step short of the returned value
Reason: Both repair routes named by the review — citing V-ReachTight (already established in this ASN) or deriving `extent_d = [0,…,0,n_s]` from TumblerSub at `zpd = m_s` — are internal derivations from claims and definitions the ASN already holds. No channel consultation is needed.
