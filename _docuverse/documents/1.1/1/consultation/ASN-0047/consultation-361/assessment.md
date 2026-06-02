# Channel Assignment — ASN-0047 review-361

**Date:** 2026-06-02 11:30

## Issue 1: Duplicated nested-node T4-legality justification (SSGU and CrossNodeAccountBase)
Reason: Pure deduplication — the fix removes a re-derived T4-legality clause and worked example in CrossNodeAccountBase, replacing it with a pointer to SSGU's existing argument. Both the justification and the divergence mechanism are already present in the ASN; no design intent or implementation evidence is needed.

## Issue 2: Near-verbatim duplication of the structural inc-chain derivation in C1c and L1c
Reason: Editorial collapse of two near-identical derivations into one shared statement, with the link case expressed as the content chain plus one extra `inc(·,0)` step. The structural difference is fully specified within the ASN; no external channel needed.

## Issue 3: Editorial flourishes in structural slots
Reason: Deletion of evaluative sentences that restate what the formal P3 statement and proof already establish. The load-bearing Gregory-cited observation is retained; the cut is internal and requires no channel.
