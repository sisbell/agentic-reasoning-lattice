# Channel Assignment — ASN-0071 review-72

**Date:** 2026-06-03 14:41

## Issue 1: Intro motivation contradicts F-CONTENT
Reason: Internal. F-CONTENT and `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` already establish that the operation matches on shared byte content, never on link addresses, and the content/link subspace split (S3★) is the ASN's own. Rewording the citation example to a transclusion/content-containment use-case follows directly from the proven scope.

## Issue 2: `vspec` silently duplicates ASN-0058's ContentReference
Reason: Internal. The relationship is derivable by comparing the two definitions already cited: vspec is ASN-0058's `ContentReference` minus well-formedness and the depth-pinning clause (iii), and `iaddrs_one` is the set-image counterpart of `resolve`/C1. Both source ASNs are available, so the cross-reference can be stated without external evidence.

## Issue 3: Procedural narration and duplicated exposition (anti-bloat)
Reason: Internal. Purely editorial deletion of roadmap/recap sentences; no design intent or implementation evidence bears on cutting meta-prose.
