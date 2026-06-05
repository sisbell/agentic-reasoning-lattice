# Channel Assignment — ASN-0103 review-17

**Date:** 2026-06-05 02:08

## Issue 1: `sig(·) = #(·)` asserted from TA5(c), but that identity requires T4-validity (TA5-SigValid)
Reason: The fix is purely internal — it threads existing foundation lemmas (TA5-SigValid, plus the T4-validity of baptized entities via B10/B6 and S7d/M0) that the ASN already cites or has established. No design intent or implementation evidence is at stake; the reviewer specifies the exact citation chain to insert.
