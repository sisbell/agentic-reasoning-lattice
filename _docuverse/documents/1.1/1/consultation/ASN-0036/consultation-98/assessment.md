# Channel Assignment — ASN-0036 review-98

**Date:** 2026-05-11 13:44

## Issue 1: Auxiliary lemma's position-preservation attribution
Reason: Purely an internal rephrasing issue — the fix requires correcting the attribution from "by (iii)" to "by (ii) and (iii)" using reasoning already present in the proof (zero-position preservation plus length preservation jointly place E at the same positions). No design intent or implementation evidence needed.

## Issue 2: subspace_I lacks standalone Formal Contract
Reason: Structural/formatting fix — add a Formal Contract block paralleling the existing `subspace` contract, drawing preconditions (S7b, S7c) and postconditions directly from material already in the ASN. No external input needed.

## Issue 3: S5 cross-document construction uses identical v_i across documents
Reason: Expository/proof-construction choice between simplifying (single shared `v = [1, 1]`) or strengthening (document-specific V-positions); both options are fully justified by the ASN's existing content (S8a, T3, T4). No design intent or implementation evidence required.
