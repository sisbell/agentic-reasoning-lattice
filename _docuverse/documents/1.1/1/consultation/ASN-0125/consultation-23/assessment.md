# Channel Assignment — ASN-0125 review-23

**Date:** 2026-06-13 15:46

## Issue 1: EL7(ii) cites the wrong Open Question
Reason: Internal. Counting the Open Questions list in the ASN shows the edit-listing question is the 8th, not the 7th; the fix is to reference by content or renumber and correct — entirely verifiable from the ASN's own text, no design intent or implementation evidence at stake.

## Issue 2: EL6(iv) opens with structure-announcing meta-prose
Reason: Internal. Pure prose edit — the two frame results being previewed are already stated in the same clause, so dropping the framing sentence requires nothing beyond the existing text.

## Issue 3: EL3's necessity proof closes with design-cost essay
Reason: Internal. Relocating the cost remark's germ ("refinements under a common prefix stay jointly queryable, but the root must be agreed") into RQ6 / the prefix-rooted-subtype-closure Open Question is a structural move of content already grounded in L10, which the ASN cites; no new design or implementation fact is needed.

## Issue 4: the ASN-0042 principal-resolution deferral is stated twice, with overlay speculation
Reason: Internal. The fix is de-duplication plus *removal* of out-of-scope overlay speculation ("owner domains span many documents"), retaining only the narrower substrate fact (per-home/per-document-chain latest is state-recoverable, per-principal is not) that this ASN already proves in EL13 — we are deleting an ASN-0042 claim, not verifying one, so no ownership-layer channel is required.
