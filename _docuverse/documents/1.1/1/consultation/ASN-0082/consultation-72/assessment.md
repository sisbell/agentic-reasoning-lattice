# Channel Assignment — ASN-0082 review-72

**Date:** 2026-05-30 13:50

## Issue 1: Interpretive restatement prose duplicates the lemmas it follows
Reason: Pure prose deletion — the TS1/TS2 citations already carry the argument and the paragraphs to be removed add no new claim. No design intent or implementation evidence is at stake.

## Issue 2: Dangling Q-references break self-containment
Reason: The fix is to drop the external Q-labels and either delete the groundings or keep the inline quote text, which is already present in the ASN ("in its original relative order on either side", [LM 4/30], [LM 4/11]). Self-containment is achieved by rewriting against existing content; no new design intent needs to be sourced.

## Issue 3: Near-duplicate boilerplate in the two cross-subspace worked examples
Reason: Editorial deduplication — factor the shared setup or trim the second example's narration. Both examples already exist in the ASN; the change is purely structural with no external dependency.
