# Channel Assignment — ASN-0047 review-357

**Date:** 2026-06-02 10:03

## Issue 1: Depth-rebasing fork bijection is load-bearing but never exercised at differing depths
Reason: The fix is internal — the ASN already establishes that `m_new` is a free caller choice ≥ 2 (ValidFirstInsertionPosition) and defines φ as the order-preserving bijection between two D-SEQ★ sequences differing only in depth; constructing a worked example at `m_new ≠ m_old` and verifying φ/D-SEQ★/D-CTG★/D-MIN★ is mechanical from these existing definitions.

## Issue 2: "Elementary" K.μ⁻ precondition is stated in terms of properties defined two sections later
Reason: This is a document-organization issue about which layer owns the constructive precondition; both the foundation-term restatement and the relocation option are fully derivable from the ASN's own definitions of D-SEQ★, D-CTG★/D-MIN★, and the elementary/extended layering.

## Issue 3: K.δ sub-case dispatch is specified twice
Reason: Pure editorial deduplication — reducing the per-k prose in the discharge section to a pointer back to the K.δ box requires no design intent or implementation evidence, only the ASN's own existing content.
