# Channel Assignment — ASN-0115 review-72

**Date:** 2026-06-10 22:52

## Issue 1: Worked instances assert exact deliveries from under-specified or unproven singleton active sets
Reason: The fix is internal — the review itself supplies the full proof sketch for the unit-spec lemma, and every step rests on substrate facts the ASN already cites (PrefixSpanCoverage from ASN-0043, the Confinement lemma, S8-depth, S8a, Prefix-at-equal-length). Rewriting the R8/R9/R10 instances to use explicit unit specs and closing R11's `act = {v'}` step requires no design-intent ruling and no implementation evidence.
