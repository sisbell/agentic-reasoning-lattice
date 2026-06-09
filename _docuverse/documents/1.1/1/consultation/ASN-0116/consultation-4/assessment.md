# Channel Assignment — ASN-0116 review-4

**Date:** 2026-06-08 20:50

## Issue 1: New content addresses' structural invariants never discharged (I3-S7 is non-inheritable, exactly like I3-S3)
Reason: Internal. The fix mirrors the existing I3-S3 non-inheritance treatment already in the ASN and discharges S7a/S7b/C1b/C1c via K.α (ASN-0093), whose properties the ASN already cites; no design intent or implementation evidence is needed.

## Issue 2: OrdShiftHom cited at the k = 0 boundary where its precondition is unmet
Reason: Internal. Pure boundary correction — `shift(p,0) = p` is S8a by precondition, `1 ≤ k < n` by OrdShiftHom; both facts are already present in the ASN.

## Issue 3: I3-V attribution is inaccurate in the append case
Reason: Internal. The correct attribution (I3-V in the occupied case, I3-CS domain closure in the append case) follows from the ASN-0082 lemma scopes the ASN already references.
