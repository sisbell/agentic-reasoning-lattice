# Channel Assignment — ASN-0100 review-20

**Date:** 2026-05-28 12:58

## Issue 1: Atomicity scope is stated as "precisely two-fold" but the K.ρ-commutation argument requires R to also be protected
Reason: The fix is internal: the contradiction is between the spec's own statements, and all three resolution options turn on the precise semantics of J1'★ (already defined in the cited ASN-0047) and the canonical ordering INSERT already specifies — no design intent or implementation evidence is required to decide whether R needs explicit envelope inclusion, whether the commutation flexibility is load-bearing, or whether J1'★ is a per-composite coupling.
