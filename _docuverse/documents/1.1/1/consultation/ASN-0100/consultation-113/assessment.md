# Channel Assignment — ASN-0100 review-113

**Date:** 2026-06-07 23:24

## Issue 1: The "identity by allocation, not value" theme is stated three times in different words
Reason: Purely editorial deduplication — the ASN already contains the formal treatment, the corollary, and the claim row; deciding which restatement to trim requires no design intent or implementation evidence.

## Issue 2: "What is *not* allocated" restates the Frame Conditions
Reason: Internal restructuring — the frame facts and the one genuinely new fact (footprint of n content-subspace addresses) are both already present in the ASN; folding and deleting needs no external input.

## Issue 3: Forward-reference deferral for INS.proj
Reason: The `d' ≠ d` case is trivially the cross-document frame already established in the same paragraph; collapsing the forward reference is derivable from the ASN's own content.
