# Channel Assignment — ASN-0099 review-16

**Date:** 2026-05-26 20:50

## Issue 1: F4's "Any other refinement" hedging contradicts itself
Reason: Pure internal logic fix. The reviewer has correctly identified the self-contradiction (the singleton-`I` canonical-span pair is itself a witness against the "finite coverage" P), and resolving it requires only rewriting the abstract-minimality argument within the ASN's own definitional vocabulary. No design intent or implementation evidence bears on the fix.

## Issue 2: F4 witness realizability under-cited
Reason: Pure citation fix internal to the substrate. The reviewer has already named the correct ASN-0043 lemmas (L9 TypeGhostPermission, L11b NonInjectivity) that supply link-configuration realizability; the ASN need only cite them alongside L4. Nothing about Nelson's design intent or Gregory's implementation behavior is in play — this is a substrate-internal precision issue.

## Issue 3: F12 labeled as a theorem but stated as a definition
Reason: Pure presentation/structural fix. F12 is the only definition of `findlinks_V` in the ASN and downstream derivations consume it definitionally; the fix is to relabel/reframe it accordingly. No external channel is needed for a labeling decision internal to this ASN's claims structure.
