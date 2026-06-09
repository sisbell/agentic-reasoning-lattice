# Channel Assignment — ASN-0117 review-19

**Date:** 2026-06-09 09:53

## Issue 1: P5 (DocumentIsolation) asserts every other document's V-positions resolve into the content store — false for any document with links
Reason: The fix is internal — the ASN already states the correct pattern (restricting resolution to content-subspace positions, or using `dom(C') ∪ dom(L')`) in "The document remains one coherent sequence," citing S3★ (ASN-0047) and SD (ASN-0093). No design intent or implementation evidence is needed; this is a consistency repair against the note's own cited foundations.

## Issue 2: Post-state range decomposition restated in two sections (anti-bloat)
Reason: Purely editorial deduplication — consolidate the range decomposition to one site and cite it from the other. Derivable from the ASN alone; no channel needed.
