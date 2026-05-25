# Channel Assignment — ASN-0075 review-11

**Date:** 2026-05-25 16:03

## Issue 1: Different-origin case in D-ACT conflates two distinct sub-cases
Reason: The fix is derivable from the ASN's own argument structure plus already-cited foundation machinery (T1, PrefixOrderingExtension, `b_C` from ASN-0034/0036). The reviewer's suggested path (appeal to `b_C(d) < b_C(d')` via the zero separator) uses only foundation primitives the ASN already invokes.

## Issue 2: wp(SHOWDELETIONS, Q0) derivation elides the subspace step
Reason: D-EXH within the same ASN already unpacks the L14 + S3★-aux + S3★ contrapositive chain needed to license the P4★ application. The fix is purely internal — either inline the chain or cite D-EXH by name.

## Issue 3: D-ACT's "consumed without information loss" claim is unsupported
Reason: The reconstruction formula and maximality framing rely only on ASN-0034's OrdinalShift constraints and the partition uniqueness D-ACT already establishes. The fix is derivable from the ASN's own content and the foundation it already cites.
