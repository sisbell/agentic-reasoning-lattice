# Channel Assignment — ASN-0086 review-155

**Date:** 2026-06-01 04:47

## Issue 1: wp Case 1 produces no weakest precondition — extended analysis lands on "left open"
Reason: The fix is editorial — either compute the wp or compress to a one-line remark — and both options draw only on definitions, the antichain, and the emission rule already present in the ASN. No design intent or implementation evidence is at stake.

## Issue 2: the non-fixpoint / restoration-by-reemission point is restated across four locations
Reason: Pure deduplication of two paragraphs already in the ASN; deciding which statement to keep and which to trim requires only the note's own text, no external channel.

## Issue 3: two conformance definitions defer to the same downstream Remark
Reason: Reordering — moving the NestedLinkWitness construction ahead of the two definitions — is a self-contained structural edit using content already present in the ASN.
