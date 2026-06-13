# Channel Assignment — ASN-0123 review-23

**Date:** 2026-06-13 08:15

## Issue 1: Body-dependency integration audit
Reason: The O5(ii) maximality gap and the ASN-0036 citation are internal — the note's own O1a + Z-mono reasoning (already worked concretely in V9w's cross-owner instance: "every prefix of `v` longer than `pfx(π)` carries `zeros ≥ 2`… so `π` is the maximal coverer") proves no principal can cover a document-tier `v` more specifically than its account-tier allocator, so maximality and the single-K.δ claim follow from ASN-0047's K.δ postconditions and ASN-0042's O5 already in hand. Only the V6 unbounded-depth conformance claim needs Nelson: whether a fixed implementation cap is nonconformant turns on whether the design mandates genuinely unbounded tumbler subdivision (the implementation side — NPLACES=16, fatal overflow — is already captured in deviation 1).
Nelson question: Does the design require version-chain (fork) depth to be genuinely unbounded — making any fixed cap on tumbler length nonconformant — or is unbounded depth an idealization that a sufficiently large finite bound conforms to?
