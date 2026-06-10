# Channel Assignment — ASN-0119 review-41

**Date:** 2026-06-10 07:57

## Issue 1: Link-subspace per-subspace arrangement invariants are not discharged
Reason: Internal fix. Everything needed is already established and cited in the ASN: RA2 leaves `V_{s_L}(d)` unchanged as a key set, R-NS (already invoked in the S3★ derivation) freezes the values on `s_L` pointwise, and the set-invariance argument the note already runs for `V_{s_C}(d)` applies verbatim to `V_{s_L}(d)`. The per-subspace quantification structure of D-CTG★/D-SEQ★/D-MIN★/S8-depth and the whole-arrangement scope of S8a/S8-fin are definitional facts about ASN-0047's invariant package, already referenced — no design intent or implementation evidence is in question.
