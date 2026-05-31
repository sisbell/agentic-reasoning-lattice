# Channel Assignment — ASN-0043 review-172

**Date:** 2026-05-31 03:08

## Issue 1: L1c's chain condition encodes only the k=2 zero-count guard, omitting the k=1 guard that "T10a-conforming" requires
Reason: The fix is internal — both remedies (add the companion `k=1` conjunct, or note it is auto-discharged by inductively-maintained T4-validity) rest entirely on TA5a, T10a.4, and T4-validity reasoning already present in the ASN. No design intent or implementation evidence is at stake.
