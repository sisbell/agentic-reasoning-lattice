# Review of ASN-0053

## REVISE

### Issue 1: TA-LC cited from non-foundation ASN-0055

**ASN-0053, S5 (SplitWidthComposition) and Properties table**: "The composition property below depends on left cancellation of TumblerAdd: if a ⊕ x = a ⊕ y with both sides well-defined, then x = y (TA-LC, ASN-0055)."

**Problem**: TA-LC (LeftCancellation) is defined in ASN-0034, which is a verified foundation ASN. The citation attributes it to ASN-0055, which is not a foundation ASN. This violates the self-containment rule: cross-ASN references are permitted only to foundation ASNs. The Properties table repeats the error: "TA-LC | ... (LeftCancellation, ASN-0055) | cited".

**Required**: Change "(TA-LC, ASN-0055)" to "(TA-LC, ASN-0034)" in both the S5 prose and the Properties Introduced table.

## OUT_OF_SCOPE

### Topic 1: Span-set difference algorithm and tight bound
**Why out of scope**: S11d establishes the tight bound of 2 for pairwise span difference across all SC cases. The natural extension — what is the tight bound on |normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)| for normalized span-sets? — is new territory already identified in the Open Questions. Not an error in this ASN.

### Topic 2: Cross-level span operations
**Why out of scope**: The ASN correctly restricts all constructive operations (S1, S3, S4, S8) to level-uniform, level-compatible spans. What happens at mixed depths is identified in the Open Questions and falls outside this ASN's scope.

VERDICT: REVISE
