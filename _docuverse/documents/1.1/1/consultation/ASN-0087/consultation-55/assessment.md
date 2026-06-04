# Channel Assignment — ASN-0087 review-55

**Date:** 2026-06-04 01:36

## Issue 1: Defensive "genuine vs derived precondition" meta-prose
Reason: Purely a prose-tightening edit — collapse the meta-framing into one line stating M-Pre with freshness/shape marked derived. The substantive content (precondition is K.λ's; freshness/shape are ASN-0093 lemmas) is already present in the ASN; no design intent or implementation evidence is needed.

## Issue 2: Redundant freshness derivation
Reason: Deduplication of two passages that establish the same fact from the same cited lemmas. The fix is to keep the case-split in one location and cross-reference from the other — entirely internal to the ASN's existing content.

## Issue 3: D-CTG★ asserted by bare phrase, discharge left implicit
Reason: The actual discharge (the D-SEQ★ set computation) already exists in the ASN; the fix only redirects the table entry to it and notes the discharge direction to avoid circularity. No external channel needed.
