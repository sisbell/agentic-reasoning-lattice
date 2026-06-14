# Channel Assignment — ASN-0131 review-70

**Date:** 2026-06-14 10:59

## Issue 1: The "higher-arity retraction links are immaterial to `nullified`" fact is restated three times, twice in one paragraph
Reason: Pure deduplication of a fact already established in ASN-0086 and cited within the note; collapsing three restatements to one placement at RE-ADDR requires no design intent or implementation evidence, only the note's own structure.

## Issue 2: Addressability infrastructure is front-loaded into the answer-definition section, declared "throughout," and carries a use-site lemma inventory
Reason: The fix is relocation and dependency-scoping — the review already enumerates which claims consume the discipline commitment (RE-ADDR/RE-RET/fresh-emission RE-EDIT) versus which are independent, and that partition is read off the note's own claim dependencies. No external channel needed.

## Issue 3: `R` is overloaded despite the stated reservation
Reason: Pure notation hygiene — completing the Θ-renaming or relabeling the K.μ⁻ retention set, and dropping the false reservation claim — fully internal to the note's symbol usage, needing neither design intent nor implementation evidence.
