# Channel Assignment — ASN-0103 review-37

**Date:** 2026-06-08 09:42

## Issue 1: Distinctness proof does not cover "every other document address"
Reason: Internal fix. The required correction is to restate the existing B7 (ASN-0040) instantiation once over all B6-valid parent–depth pairs `(p',d') ≠ (A,2)` — a generalization of reasoning already in the proof, derivable from the ASN's own machinery.

## Issue 2: CND.no-sharing overreaches into out-of-scope content allocation and is false under transclusion
Reason: Internal fix. The remedy is to restrict the claim to the in-scope post-state fact `ran(M'(d)) = ∅` (already CND.empty) and drop the future-content reasoning; the ASN's own content (CND.empty, the out-of-scope boundary on INSERT/COPY) supplies everything needed.

## Issue 3: forking-contrast section is essay + repeated out-of-scope deferral
Reason: Internal anti-bloat edit. Collapse to the one in-scope residue `ran(M'(d)) = ∅` from Effect Two; no external intent or implementation evidence is required to delete deferred forking prose.

## Issue 4: frame restated three times verbatim
Reason: Internal anti-bloat edit. Replace the third frame restatement with a reference to the Formal Contract's Effect; purely a structural deduplication within the ASN.
