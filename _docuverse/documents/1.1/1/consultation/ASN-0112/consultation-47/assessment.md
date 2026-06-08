# Channel Assignment — ASN-0112 review-47

**Date:** 2026-06-08 12:35

## Issue 1: Level-uniformity of the returned span never characterized
Reason: Fully derivable from the ASN. The level-uniformity status follows from `#extent_d = max(#origin_d, #reach_d)` against S6 (ASN-0053), using the exact `#origin_d` vs `#reach_d` depth analysis already discharged in V2 and V-ReachTight. No external evidence or intent needed.

## Issue 2: V18 accretes redundant framing around V8 and defers within the document
Reason: Internal restructuring. Consolidating V8/V18/V11 is a prose reorganization, and the editing-transition vocabulary (K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~) is the spec's own operation set; the exhaustiveness claim is checked against those operation ASNs already in the foundation, not against design intent or implementation.

## Issue 3: Ghost-element analogy conflates two distinct concepts in V11
Reason: Internal correction. The fix is to drop the element-level "ghost element" term (ASN-0040 B3) or restate the empty-document case as `O(d) = ∅` for allocated `d` directly — a conceptual disambiguation resolvable from the cited foundation and this ASN's own definitions.
