# Channel Assignment — ASN-0053 review-47

**Date:** 2026-05-28 21:13

## Issue 1: "Bijection" asserted as a derived guarantee without derivation, conflating ordered and unordered pairs
Reason: The fix is purely internal — it turns on whether S4a + S3b actually establish a bijection over ordered vs. unordered adjacent pairs, which is settled entirely by the ASN's own lemma statements (S4 produces ordered ⟨λ, ρ⟩; S3b recovers the unordered {α, β}). Neither design intent nor implementation evidence bears on whether to tighten the codomain or delete the sentence.
