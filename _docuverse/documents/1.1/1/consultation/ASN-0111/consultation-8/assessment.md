# Channel Assignment — ASN-0111 review-8

**Date:** 2026-06-07 23:39

## Issue 1: Orphaned-instance slot-1 argument silently widens the supposition
Reason: The required fix is a formal derivation chaining lemmas the note already cites — ChainDiscipline/FirstEmission (ASN-0093), L0 and T7 (ASN-0043/0034), S3★ (ASN-0047). No design intent or implementation evidence is at stake; exhaustiveness of the three content addresses and the empty `dom(Σ.L)` intersection follow mechanically from the substrate invariants. Internal.

## Issue 2: Orphaned-instance slot-3 "meets neither store" under-argued for the link store
Reason: The missing `dom(Σ.L)` half is a pure subspace-disjointness argument from L0 (ASN-0043) and T7 (ASN-0034), both already in scope. The conclusion is forced by the address algebra, requiring neither Nelson's intent nor Gregory's code. Internal.
