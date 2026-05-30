# Channel Assignment — ASN-0042 review-101

**Date:** 2026-05-30 02:59

## Issue 1: Repeated back-reference to "the single allocation point corroborated at O17b"
Reason: Purely editorial deduplication — the fix deletes three non-load-bearing back-references whose corroboration is already established at O17b. No design intent or implementation evidence is needed; the host proofs (O18, DelegatorAllocatesPrefix, O10) are discharged by abstract argument already present in the ASN.

## Issue 2: Covering-chain comparability re-derived inline where parallel proofs cite the lemma
Reason: Internal consistency fix — the covering-chain lemma is already stated and proved in the ASN, and parallel proofs already cite it; replacing the two inline re-derivations with citations uses only material present in the document.
