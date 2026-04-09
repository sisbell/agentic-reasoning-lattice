# Revision Categorization — ASN-0043 review-43

**Date:** 2026-04-09 16:13

## Issue 1: L11b proof cites T9 for freshness — should cite GlobalUniqueness
Category: INTERNAL
Reason: The correct derivation chain (L1c → T10a → GlobalUniqueness) is already explicitly stated in L11a within the same ASN. The fix is replacing one citation with another.

## Issue 2: L0 disjointness derivation has uncited dependency on L1 and S7b
Category: INTERNAL
Reason: Both L1 and S7b are already present in the ASN and its stated dependency (ASN-0036). The fix is either reordering L1 before L0 or adding an explicit forward-reference annotation — no external evidence needed.

## Issue 3: L14a omitted from L9 and L11b invariant verification
Category: INTERNAL
Reason: The ASN already states that L14a follows from S3 + L0, and both proofs already verify S3 and L0. The fix is adding one line to each verification list citing the existing derivation.

## Issue 4: Worked example omits L1c verification
Category: INTERNAL
Reason: The review itself sketches the allocator path, and all required definitions (T10a, TA5a, `inc`) are in ASN-0034. The fix is tracing the allocation steps already implicit in the example's address choices.
