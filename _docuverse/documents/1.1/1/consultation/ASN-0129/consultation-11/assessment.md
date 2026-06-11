# Channel Assignment — ASN-0129 review-11

**Date:** 2026-06-11 16:53

## Issue 1: QD-audit grounds a membership test, then grants an enumeration
Reason: The required fix forks on whether an enumeration warrant exists in either authority — the note's own audit method ("measured against the upstream read surface," with the two-authority pattern used for `Reg` and `dom(Σ.C)`) demands both design intent and implementation evidence before choosing between grounding the enumeration or downgrading to the membership-only alternative.
Nelson question: Does the design treat the set of all documents as an enumerable, queryable domain (a directory or census of the docuverse), or are documents only ever addressed individually by a caller who already holds their addresses?
Gregory question: Does any read operation in udanax-green enumerate the set of stored documents (listing document keys from the granfilade or equivalent), or is the document store consulted on the read path only as an existence/membership check against a caller-supplied address?

## Issue 2: V-IDX argues a case its own premises exclude
Reason: The fix is internal — the inspection argument (`R`'s record attaches no behavior family, per S3/R-C1 already cited in the note) suffices, and the change is deleting the redundant R-C0 foreclosure walk or, at the author's option, stating a robustness intent; no design-intent or implementation fact is missing.

## Issue 3: the vocabulary section audits itself
Reason: The fix is internal — pure compression and deduplication of prose whose content already exists at its proper sites (QD-audit, PC6); the duplicated Gregory read-path evidence is to be stated once, not re-verified.

## Issue 4: QD-audit's content-store entry carries a prior excision as advocacy
Reason: The fix is internal — the boundary facts to retain (no upstream contract consults `dom(Σ.C)`; content is reached only through arrangement reads, ASN-0127's layer) are already stated and undisputed; the change is deleting the write-path forensics and advocacy framing.

## Issue 5: the state index is dropped inconsistently across signatures
Reason: The fix is internal — `S` is fixed by the upstream chain the note already cites (ASN-0128's reachable extended-record states), the signature convention and fold-body correction are mechanical, and the per-I0-class qualification is disambiguation the I1a citation already supplies.
