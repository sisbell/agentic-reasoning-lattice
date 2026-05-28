# Channel Assignment — ASN-0077 review-39

**Date:** 2026-05-28 12:03

## Issue 1: K.σ is referenced but undefined in any foundation ASN
Reason: This is a self-containment/exhaustiveness fix. The complete transition vocabulary is fixed by the foundation ASNs (0047 K-operations) already cited as dependencies; the resolution (restrict the multi-step lemmas to foundation vocabulary or drop the bare K.σ reference) is derivable from the ASN's own dependency set without design intent or implementation evidence.

## Issue 2: Singleton I-span edge case over-claims the intersection and discharges it via vocabulary closure
Reason: The reviewer supplies the fix path — weaken to the single-origin result (`origins_I(Σ, σ_a) = {origin(a)}`), which O5/O9 and the `origin` projection already deliver without any allocator-length closure. The over-claimed strict singleton is not needed, so the correction is internal to the ASN.

## Issue 3: Internal inconsistency in the attribution of O0(b) for dom(L)
Reason: Purely an internal consistency repair — the Summary must be reconciled with the O0(b) derivation and the Claims-Introduced table (L1c + Allocator hierarchy + SubAllocatorAxiom, dropping the K.λ-event credit). No external channel bears on a self-contradiction within the ASN.

## Issue 4: O3's V-span computability claim leans on a state invariant
Reason: The fix follows from the ASN's own definitions — `origin` is total on any tumbler with `zeros ≥ 2` (T4b projection), so well-definedness needs no S3★ state read. Restating that, or softening the "from the restriction alone" phrasing, is derivable internally.
