# Channel Assignment — ASN-0047 review-364

**Date:** 2026-06-02 12:15

## Issue 1: P7a "derivation" box is a forward pointer that duplicates the Class (b) argument
Reason: Purely editorial deduplication — the witness chain (J0→S3★+L14→J1★) is already stated in full in the Class (b) proof; collapsing the Cross-layer box to a pointer requires no design intent or implementation evidence.

## Issue 2: Defensive anti-circularity prose in K.μ⁻ admissible-contraction-shape reverse direction
Reason: Removing the "not on X / not from Y" disclaimers and stating the hypothesis once is a prose tightening; the derivation itself is fully present in the ASN, so no channel is needed.

## Issue 3: SubAllocatorBundle glossary row is an essay / use-site inventory in a structural slot
Reason: Compressing the glossary row to a property statement plus a pointer to the definition box is a structural edit; the lemma inventory already lives in the definition box, so the fix is internal.
