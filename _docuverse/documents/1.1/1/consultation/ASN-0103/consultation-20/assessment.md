# Channel Assignment — ASN-0103 review-20

**Date:** 2026-06-05 02:39

## Issue 1: O5 invoked as authority over a registry-free state model
Reason: Internal fix — the ASN already establishes the deferral discipline (declining the ω-valued claim because B/Π are absent from `(C,L,E,M,R)`), and the required fix is to apply that same discipline to O5, either as a stated modeling assumption parallel to CND.A-act or a deferral. No design intent or implementation evidence is needed.

## Issue 2: Freshness `d ∉ E` not closed for node and account entities
Reason: Internal fix — the closure is already proven in the ASN (`D_A = E ∩ S(A,2)`, `d ∈ S(A,2)`, `d > max(D_A)`), and `zeros(d)=2` excludes nodes/accounts; assembling these into the one-line freshness argument requires only the ASN's own content.
