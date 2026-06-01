# Channel Assignment — ASN-0086 review-135

**Date:** 2026-06-01 01:40

## Issue 1: wp Case 2 is labeled "weakest precondition" but `K ≁ R` is only sufficient, not necessary
Reason: Fix is internal — the counterexample (`K ~ R` with `G = ∅`) and the corrected wp formula both follow from the ASN's own definitions of `nullified`, `coverage`, and `A_K`; no design intent or implementation evidence is required to relabel or restate the precondition.

## Issue 2: The at-most-one-key-per-home / frontier-landing discipline is restated three times in different words
Reason: Fix is internal — purely an editorial deduplication, stating the discipline once in the Definition and citing it by name in R0a-Cor1 and R7a; no external input needed.

## Issue 3: Definition — state-local-conforming state carries an inline worked counterexample in a definition slot
Reason: Fix is internal — relocating the `a'' = inc(a, 1)` witness to a named remark and pointing the definition to it is a structural reorganization derivable from the ASN alone.
