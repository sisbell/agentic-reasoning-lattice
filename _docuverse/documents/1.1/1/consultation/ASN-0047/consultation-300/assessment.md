# Channel Assignment — ASN-0047 review-300

**Date:** 2026-06-01 23:10

## Issue 1: The "link-subspace mappings don't participate in provenance" fact is restated in five places
Reason: This is a pure consolidation task — naming an existing consequence (link-subspace V-positions target dom(L), disjoint from dom(C) by L14, so no provenance) once and replacing four restatements with citations. Every component (S3★, L14, P7, the s_L≠s_C chain) is already present in the ASN; no design intent or implementation evidence is needed.

## Issue 2: The non-trivial `m ≥ 3` branch of D-SEQ★ is never exercised by a concrete example
Reason: The fix adds a self-contained concrete trace at m=3 that instantiates the existing Step-1 u_M contradiction argument against a specific arrangement; the derivation, S8-fin, D-CTG★, and the canonical shape are all already proved in the ASN. This is purely exercising existing proved machinery — no external channel required.
