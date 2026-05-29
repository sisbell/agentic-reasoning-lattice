# Channel Assignment — ASN-0036 review-134

**Date:** 2026-05-29 00:01

## Issue 1: S7d postcondition annotates its downstream consumer and duplicates S7's derivation
Reason: Purely structural edit — delete the use-site clause and let S7's proof cite S7d directly. The fact and its derivation are already present in the ASN; no design intent or implementation evidence is at stake.

## Issue 2: the `m ≥ 2` deferral to Open Questions is restated across multiple slots
Reason: Editorial deduplication — state `m ≥ 2` once and remove the Signature-line restatement. The content already exists in the ASN; nothing external is required.

## Issue 3: implementation evidence for S7a parked in the S7 proof section
Reason: Relocation/deletion of a sentence that already exists in the ASN; S7a is already substantiated by its own evidence. The choice to move or drop is internal and needs no new consultation.

## Issue 4: `subspace_I` carries a full formal contract but is load-bearing in no proof
Reason: Internal restructuring — inline the projection at its single use or downgrade the contract to a comment. Whether any proof depends on it is determinable by inspecting the ASN itself.

## Issue 5: S8's conjunct (b) is vacuous in the exhibited witness, so the named theorem over-promises
Reason: Contract-wording fix — foreground the disjoint-partition result the proof actually establishes and state that (b) holds only at the base case. The proof's true content is already in the ASN; this is internal rephrasing.
