# Channel Assignment — ASN-0129 review-9

**Date:** 2026-06-11 15:52

## Issue 1: V_atom's displayed definition omits two of its four announced additions
Reason: Internal fix. The four additions, their definitions, and their downstream uses are all already in the ASN; the fix is to restate the alphabet union once (`⋃_K Tpl(record(K)) ∪ V-TUP ∪ V-PRIM`), classify V-AUD as new view-readings of existing core symbols (which the core atoms' existing `view` parameter already supports), and delete the corrective parentheticals — pure definitional bookkeeping requiring no design intent or implementation evidence.

## Issue 2: the parity example is a vocabulary-axis escape mislabeled as feedback
Reason: Internal fix. The misclassification is decided entirely by the ASN's own definitions — its feedback criterion ("depth no syntax fixes") and its admitted fold forms (PC1/PC2a) — and the relabeled example still carries the non-implication argument unchanged, since parity remains unrestricted-computable and plausibly outside PL's ℕ fragment; scoping "benign" to node combinators versus new fold forms is a precision edit on the note's own taxonomy, not a question about Nelson's design or Gregory's read path.

## Issue 3: admission rationales repeated at every definition site, all deferring to PC6's converse
Reason: Internal fix. This is pure prose consolidation — every rationale's technical content is already established at PC6's converse, and the fix is deleting the per-site duplicates; no new facts from either channel are required.

## Issue 4: front matter re-argues body content at full technical depth
Reason: Internal fix. The fix is editorial compression of the intro and commitments bullets into indices pointing at body sites where each argument already lives in full; no design-intent or implementation question arises.
