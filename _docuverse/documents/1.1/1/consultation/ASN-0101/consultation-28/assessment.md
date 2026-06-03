# Channel Assignment — ASN-0101 review-28

**Date:** 2026-06-03 16:27

## Issue 1: Worked-example wp statements drop the enabledness conjunct that D11 makes load-bearing
Reason: Internal fix. D11 already establishes the canonical wp form with the `enabled(DEL[d, σ]) ∧ (pullback)` guard and justifies its necessity; the worked-example statements simply need to be brought into line with the ASN's own definition. No design intent or implementation evidence is required.

## Issue 2: LP-family catalogue mis-names LP11
Reason: Internal fix. The correct lemma names belong to ASN-0098 within the spec corpus, not to Nelson's design intent or Gregory's implementation; the correction is a cross-reference lookup against the sibling ASN, derivable without either channel.
