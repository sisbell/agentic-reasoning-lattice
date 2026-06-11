# Channel Assignment — ASN-0112 review-59

**Date:** 2026-06-10 23:36

## Issue 1: The `m_C < m_L` configuration — the only non-level-uniform regime — is claimed but never instantiated
Reason: The fix is internal — the variant is pure tumbler arithmetic (TumblerSub/TumblerAdd, D1 round-trip) already specified by the ASN's own machinery, the review supplies concrete witness values (`o = [1,1]`, `max O(d) = [2,1,1]`), and reachability is already settled by ValidFirstLinkPosition; no design-intent or implementation evidence is required to work the example.

## Issue 2: Defensive discharge framing and intra-paragraph restatement around the occupied-depth definition (anti-bloat)
Reason: The fix is internal — it is a pure prose deletion preserving identified load-bearing clauses, requiring only the ASN's existing text to execute; no semantic content changes, so neither design intent nor implementation evidence bears on it.
