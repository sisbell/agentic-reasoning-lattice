# Channel Assignment — ASN-0114 review-1

**Date:** 2026-06-04 23:16

## Issue 1: No concrete worked example verifying the postconditions
Reason: Internal. The fix instantiates existing claims against a constructed link using definitions already in the ASN (coverage, span-set, Endset); the candidate witnesses (`orglinks.c:412–413`, `sporgl.c:93`) are already cited, so no new evidence is required to build the worked instance.

## Issue 2: `followlink(Σ, a, i)` is used both as a non-deterministic relation and as a determinate value
Reason: Internal. The function-vs-relation choice is a specification modeling decision; realizability of `R` is a one-line consequence of the substrate (`Endset = 𝒫_fin(Span)`); and the `⟨⟩` uniqueness justification needs only ASN-0053 S2, an already-referenced dependency — all derivable without Nelson or Gregory.

## Issue 3: F5's derivation overstates which premises are load-bearing
Reason: Internal. The review has already diagnosed the prose/formal mismatch and supplied the correction; aligning F5's prose with its coverage-equality statement (L12 alone is load-bearing; content-identity supports a separate, stronger material-permanence reading) requires only the ASN's own claims.
