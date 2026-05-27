# Channel Assignment — ASN-0100 review-4

**Date:** 2026-05-27 13:22

## Issue 1: I3-C citation does not match INSERT's content frame
Reason: Citation/internal consistency issue — INS.C and S0/P0 already establish the correct (weaker) content frame within the ASN. The fix is to remove or rephrase the I3-C citation; no external channel input is needed.

## Issue 2: Imprecise citations for shift last-component arithmetic in S2 disjointness proof
Reason: Pure citation precision fix — the correct lemmas (TumblerAdd in ASN-0034, OrdAddHom (a) in ASN-0036) are already established and cited elsewhere in the ASN. Replacement is mechanical and derivable from the existing formal apparatus.

## Issue 3: Missing explicit Insertion-region carve-out for I3-VD, I3-VP, I3-fin, I3-S7
Reason: Presentational/structural fix — the Insertion-region verification of S8-depth, S8a, S8-fin, and S7 invariants follows from existing arguments in the ASN (e.g., the empty-case S8a verification, TumblerAdd's result-length identity, OrdAddHom). The fix is to factor these out explicitly and parallel the I3-S2 / I3-S3 carve-out pattern.
