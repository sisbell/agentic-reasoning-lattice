# Channel Assignment — ASN-0042 review-124

**Date:** 2026-05-30 05:33

## Issue 1: T4-discharge convention promises non-restatement, then is restated at every use site
Reason: Purely an internal editorial deduplication — choose to keep either the convention paragraph or the inline discharges and strip the redundant copy. No design intent or implementation evidence bears on which copy survives; the discharge mechanism (T4 via O17) is already fixed within the ASN.

## Issue 2: Duplicated state-relativization notation
Reason: Internal — two passages state the same notational abbreviation; the fix is to delete one. Nothing about design or implementation is at stake in choosing which to remove.

## Issue 3: O10(b) asserts a content-invariance guarantee the ownership model cannot establish
Reason: Internal — the ASN's own Scope section lists the content model as out of scope and the O10 proof discharges only registry persistence (B0) and effective-owner invariance, so the "no content is modified" claim is unprovable here by the ASN's own boundaries. The fix is to drop or reframe the phrase as an explicit frame observation, derivable from the ASN's existing scope statement and formal postcondition.
