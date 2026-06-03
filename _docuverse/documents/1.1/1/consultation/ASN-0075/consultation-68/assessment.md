# Channel Assignment — ASN-0075 review-68

**Date:** 2026-06-03 11:07

## Issue 1: D-ORD named "Order Preservation" but preserves no order
Reason: Purely internal — the fix renames a claim and restates it to match content already present in the ASN (output is a T1-orderable finite subset, with the V-order disclaimer already written). No design intent or implementation evidence bears on what to call the claim.

## Issue 2: wp/termination analysis depends on claims stated later
Reason: Purely internal — a reordering/self-containment fix. The needed premises (C-fin, S8-fin, P7, D-OBS's no-write property) are all already in the ASN; resolving the forward reference requires only moving or restating existing content.
