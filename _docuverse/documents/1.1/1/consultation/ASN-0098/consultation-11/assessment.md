# Channel Assignment — ASN-0098 review-11

**Date:** 2026-05-25 23:39

## Issue 1: Cross-subspace tightness case missing in achievability argument
Reason: The fix is fully derivable from the ASN's own foundations — the review supplies the argument structure (s_C vs s_L divergence at position #d_0 + 2, with TumblerAdd prefix-copy and T1 case (i)), and all cited machinery (SC-NEQ, TumblerAdd, chain structure of A_L(d_0)) is already in scope from ASN-0034/0093.

## Issue 2: Loose operation descriptions in descendant/ancestor cases
Reason: The review diagnoses the misstatement and offers a structural reframe whose justification (induction on length difference, structural form from T4-validity and zeros-count preservation) is already in scope from ASN-0034 and ASN-0047. The existing proof body already proceeds structurally; only the prose preamble needs correction.

## Issue 3: v_ℓ ∉ dom(Σ.M(d)) asserted without derivation in LP9
Reason: Both fix options offered by the review (cite K.μ⁺_L's effect clause, or walk through the two-sub-case argument using D-MIN★, subspace divergence, and TS4) rely entirely on formal material already cited from ASN-0034 and ASN-0047. No design-intent or implementation-evidence question arises.

## Issue 4: Reference-frame remark overstates invariance
Reason: The fix is a prose-accuracy correction about the relationship between ASN-0036, ASN-0047, and ASN-0093 — all peer spec ASNs whose contents (S3 vs S3★, presence/absence of K.μ⁺_L) are knowable from the ASN's own corpus. No external channel is required to identify the working frame correctly.
