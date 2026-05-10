# Review of ASN-0043

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage as foundation-level lemma
**Why out of scope**: PrefixSpanCoverage is a general result about tumbler arithmetic — the unit-depth span at any tumbler covers exactly its prefix-extension set. Nothing in the proof or statement references links. Moving it to ASN-0034 (or a span algebra ASN) would make it reusable by future ASNs without cross-reference. The proof here is correct; the placement is an organizational concern for later work.

### Topic 2: V-space representation of links
**Why out of scope**: The implementation assigns V-positions to link endsets within each document (V-addresses 1.1, 2.1, 3.1 for from/to/type). How these V-positions relate to `Σ.M`, and whether S3's referential integrity constraint needs generalization when link V-positions are modeled, is a question about the arrangement layer — not about what links are. The explicit scope exclusion of "POOM structure and V-stream mechanics" covers this correctly.

VERDICT: CONVERGED
