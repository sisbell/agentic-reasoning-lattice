# Review of ASN-0077

This is a mature, carefully argued ASN. The pointwise/I-span/V-span structure is sound, the proofs are detailed (the singleton-I-span case in particular discharges every length branch), foundation citations are clean (no improper cross-ASN references), and edge cases are well covered. The note carries `review-mode.anti-bloat`, and the substantive findings are accretion around the forward-reference and labeling machinery, not correctness gaps.

## REVISE

### Issue 1: Labeling archaeology and use-site inventory around (F1)/(F3)
**ASN-0077, "Lifting origin to a V-span"**: "We adopt (F1) as the definition and derive (F3) as its equivalent block-collapsed form — the only auxiliary the downstream claims (O7, O11, O12, the worked example) consume. (The labels (F1) and (F3) are retained for continuity with those downstream references; there is no intervening (F2).)"
**Problem**: The parenthetical is pure document archaeology — "retained for continuity," "no intervening (F2)" tells the reader nothing about origin. The clause "the only auxiliary the downstream claims (O7, O11, O12, the worked example) consume" is a use-site inventory enumerating downstream consumers rather than advancing the definition's meaning. The preceding sentence "The reader-facing form — the form that the operation specification will use —" carries the same forward-pointer accretion.
**Required**: Collapse to one sentence: "(F1) is the definition; (F3) is the equivalent block-collapsed form derived below via O2." Drop the (F2) remark, the "retained for continuity" clause, and the downstream-consumer inventory.

### Issue 2: DRY-refactor justification in WF_V introduction
**ASN-0077, Definition (WF_V)**: "We name them once, here, so the claims can reference the predicate rather than re-enumerating the conjuncts and re-naming them by ordinal."
**Problem**: This sentence justifies the document-organization decision (why a named predicate is introduced) rather than stating what the predicate is. It is meta-prose of the "why this is placed here" kind flagged for this note.
**Required**: Delete the sentence. The first sentence ("The preservation and admissibility claims that follow all turn on the same six well-formedness conditions") already motivates the predicate; the conjunct list does the rest.

## OUT_OF_SCOPE

The four Open Questions (unified content+link origin operation, intermediate-chain surfacing, native-vs-transcluded distinction, historical containment from Σ.R) are correctly deferred as future operations rather than gaps in this ASN. No action needed.

VERDICT: REVISE
